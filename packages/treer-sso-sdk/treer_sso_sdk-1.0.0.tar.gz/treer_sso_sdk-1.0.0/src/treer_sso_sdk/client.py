#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Treer SSO SDK主要客户端实现
"""

import json
import logging
from typing import Optional

import httpx

from .config import SSOConfig
from .exceptions import (
    SSOError,
    SSOAuthenticationError,
    SSOInvalidCodeError,
    SSOInvalidTokenError,
    SSONetworkError,
)
from .http_client import AsyncHTTPClient
from .interfaces import HTTPClientInterface, SSOClientInterface
from .models import TokenResponse, UserInfo


class TreerSSOClient(SSOClientInterface):
    """Treer SSO客户端
    
    用于与Treer SSO服务进行OAuth 2.0授权码流程交互
    支持获取访问令牌和用户信息
    
    Example:
        >>> from treer_sso_sdk import TreerSSOClient, SSOConfig
        >>> 
        >>> config = SSOConfig(
        ...     client_id="your_client_id",
        ...     client_secret="your_client_secret"
        ... )
        >>> 
        >>> async with TreerSSOClient(config) as client:
        ...     user_info = await client.get_user_info_by_code("auth_code")
        ...     print(f"用户: {user_info.username}")
    """
    
    def __init__(
        self, 
        config: SSOConfig, 
        http_client: Optional[HTTPClientInterface] = None
    ) -> None:
        """初始化SSO客户端
        
        Args:
            config: SSO配置对象
            http_client: HTTP客户端实现（可选，主要用于测试）
        """
        self.config = config
        self.http_client = http_client or AsyncHTTPClient(config)
        self.logger = logging.getLogger(__name__)
    
    async def get_access_token(
        self, 
        authorization_code: str, 
        redirect_uri: Optional[str] = None
    ) -> TokenResponse:
        """通过授权码获取访问令牌
        
        Args:
            authorization_code: OAuth 2.0授权码
            redirect_uri: 重定向URI（可选）
            
        Returns:
            TokenResponse: 包含访问令牌的响应
            
        Raises:
            SSOInvalidCodeError: 授权码无效
            SSONetworkError: 网络请求失败
            SSOAuthenticationError: 认证失败
        """
        url = f"{self.config.sso_base_url}/api/v1/oauth/token"
        
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
        }
        
        if redirect_uri:
            data["redirect_uri"] = redirect_uri
        
        try:
            self.logger.debug(f"正在获取访问令牌: {url}")
            response = await self.http_client.post(
                url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                response_data = response.json()
                
                # token接口直接返回OAuthTokenResponseDTO，不包装在ApiResponse中
                # 检查响应数据是否包含access_token（如果没有说明是错误响应）
                if "access_token" not in response_data:
                    # 可能是包装在ApiResponse中的错误响应
                    if "success" in response_data and not response_data["success"]:
                        error_code = response_data.get("code", "unknown")
                        error_message = response_data.get("message", "获取访问令牌失败")
                        
                        if error_code in ["oauth.invalid_code", "oauth.authorization_failed"]:
                            raise SSOInvalidCodeError(error_message, error_code, response_data.get("details"))
                        else:
                            raise SSOAuthenticationError(error_message, error_code, response_data.get("details"))
                    else:
                        raise SSOError("响应格式错误：缺少access_token字段")
                
                # 直接从响应数据提取令牌信息
                return TokenResponse(
                    access_token=response_data["access_token"],
                    token_type=response_data.get("token_type", "Bearer"),
                    expires_in=response_data.get("expires_in"),
                    refresh_token=response_data.get("refresh_token"),
                    scope=response_data.get("scope")
                )
            
            elif response.status_code == 400:
                error_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                raise SSOInvalidCodeError(
                    error_data.get("message", "无效的授权码"),
                    error_data.get("code", "invalid_code"),
                    error_data.get("details")
                )
            
            else:
                raise SSOAuthenticationError(
                    f"获取访问令牌失败: HTTP {response.status_code}",
                    f"http_{response.status_code}"
                )
        
        except httpx.RequestError as e:
            raise SSONetworkError(f"网络请求失败: {e}")
        except json.JSONDecodeError as e:
            raise SSOError(f"响应解析失败: {e}")
    
    async def get_user_info(self, access_token: str) -> UserInfo:
        """通过访问令牌获取用户信息
        
        Args:
            access_token: 访问令牌
            
        Returns:
            UserInfo: 用户信息
            
        Raises:
            SSOInvalidTokenError: 访问令牌无效
            SSONetworkError: 网络请求失败
        """
        url = f"{self.config.sso_base_url}/api/v1/users/me"
        
        try:
            self.logger.debug(f"正在获取用户信息: {url}")
            response = await self.http_client.get(
                url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if response.status_code == 200:
                response_data = response.json()
                
                # 检查是否是业务错误
                if not response_data.get("success", True):
                    error_code = response_data.get("code", "unknown")
                    error_message = response_data.get("message", "获取用户信息失败")
                    raise SSOError(error_message, error_code, response_data.get("details"))
                
                # 提取用户信息
                user_data = response_data.get("data", response_data)
                return UserInfo.from_dict(user_data)
            
            elif response.status_code == 401:
                error_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                raise SSOInvalidTokenError(
                    error_data.get("message", "访问令牌无效或已过期"),
                    error_data.get("code", "invalid_token"),
                    error_data.get("details")
                )
            
            else:
                raise SSOError(
                    f"获取用户信息失败: HTTP {response.status_code}",
                    f"http_{response.status_code}"
                )
        
        except httpx.RequestError as e:
            raise SSONetworkError(f"网络请求失败: {e}")
        except json.JSONDecodeError as e:
            raise SSOError(f"响应解析失败: {e}")
    
    async def get_user_info_by_code(
        self, 
        authorization_code: str, 
        redirect_uri: Optional[str] = None
    ) -> UserInfo:
        """通过授权码直接获取用户信息（一步到位）
        
        这是最常用的方法，将获取令牌和获取用户信息两个步骤合并
        
        Args:
            authorization_code: OAuth 2.0授权码
            redirect_uri: 重定向URI（可选）
            
        Returns:
            UserInfo: 用户信息
            
        Raises:
            SSOInvalidCodeError: 授权码无效
            SSOInvalidTokenError: 访问令牌无效
            SSONetworkError: 网络请求失败
            SSOAuthenticationError: 认证失败
        """
        # 步骤1: 获取访问令牌
        token_response = await self.get_access_token(authorization_code, redirect_uri)
        
        # 步骤2: 获取用户信息
        return await self.get_user_info(token_response.access_token)
    
    async def close(self) -> None:
        """关闭客户端连接"""
        await self.http_client.close()
    
    async def __aenter__(self) -> 'TreerSSOClient':
        """异步上下文管理器入口"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """异步上下文管理器出口"""
        await self.close() 