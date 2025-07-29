#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Treer SSO SDK便捷函数
"""

from typing import Optional

from .client import TreerSSOClient
from .config import SSOConfig
from .models import UserInfo


async def get_user_info_by_code(
    authorization_code: str,
    client_id: str,
    client_secret: str,
    sso_base_url: str = "https://sso-api.treer.ru",
    redirect_uri: Optional[str] = None,
    timeout: int = 30
) -> UserInfo:
    """便捷函数：直接通过授权码获取用户信息
    
    这是一个简化的函数，适合快速集成使用。对于复杂的应用场景，
    建议直接使用TreerSSOClient类。
    
    Args:
        authorization_code: OAuth 2.0授权码
        client_id: 客户端ID
        client_secret: 客户端密钥
        sso_base_url: SSO服务基础URL，默认为生产环境
        redirect_uri: 重定向URI（可选）
        timeout: 请求超时时间（秒），默认30秒
        
    Returns:
        UserInfo: 用户信息对象
        
    Raises:
        SSOConfigError: 配置错误
        SSOInvalidCodeError: 授权码无效
        SSONetworkError: 网络请求失败
        SSOAuthenticationError: 认证失败
        
    Example:
        >>> import asyncio
        >>> from treer_sso_sdk import get_user_info_by_code
        >>> 
        >>> async def main():
        ...     user_info = await get_user_info_by_code(
        ...         authorization_code="your_auth_code",
        ...         client_id="your_client_id",
        ...         client_secret="your_client_secret"
        ...     )
        ...     print(f"用户: {user_info.username}")
        ...     print(f"邮箱: {user_info.email}")
        >>> 
        >>> asyncio.run(main())
    """
    config = SSOConfig(
        client_id=client_id,
        client_secret=client_secret,
        sso_base_url=sso_base_url,
        timeout=timeout
    )
    
    async with TreerSSOClient(config) as client:
        return await client.get_user_info_by_code(authorization_code, redirect_uri) 