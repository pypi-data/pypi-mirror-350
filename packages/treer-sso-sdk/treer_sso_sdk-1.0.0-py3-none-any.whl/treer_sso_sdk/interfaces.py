#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Treer SSO SDK抽象接口定义
"""

from abc import ABC, abstractmethod
from typing import Optional
import httpx

from .models import TokenResponse, UserInfo


class HTTPClientInterface(ABC):
    """HTTP客户端接口，便于测试和扩展"""
    
    @abstractmethod
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """发送POST请求
        
        Args:
            url: 请求URL
            **kwargs: 请求参数
            
        Returns:
            HTTP响应对象
        """
        pass
    
    @abstractmethod
    async def get(self, url: str, **kwargs) -> httpx.Response:
        """发送GET请求
        
        Args:
            url: 请求URL
            **kwargs: 请求参数
            
        Returns:
            HTTP响应对象
        """
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """关闭连接"""
        pass


class SSOClientInterface(ABC):
    """SSO客户端接口"""
    
    @abstractmethod
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
        """
        pass
    
    @abstractmethod
    async def get_user_info(self, access_token: str) -> UserInfo:
        """通过访问令牌获取用户信息
        
        Args:
            access_token: 访问令牌
            
        Returns:
            UserInfo: 用户信息
        """
        pass
    
    @abstractmethod
    async def get_user_info_by_code(
        self, 
        authorization_code: str, 
        redirect_uri: Optional[str] = None
    ) -> UserInfo:
        """通过授权码直接获取用户信息（一步到位）
        
        Args:
            authorization_code: OAuth 2.0授权码
            redirect_uri: 重定向URI（可选）
            
        Returns:
            UserInfo: 用户信息
        """
        pass 