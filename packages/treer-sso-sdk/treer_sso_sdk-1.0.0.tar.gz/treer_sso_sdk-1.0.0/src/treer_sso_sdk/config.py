#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Treer SSO SDK配置类
"""

from dataclasses import dataclass
from .exceptions import SSOConfigError


@dataclass
class SSOConfig:
    """SSO配置类
    
    Args:
        client_id: OAuth 2.0客户端ID
        client_secret: OAuth 2.0客户端密钥
        sso_base_url: SSO服务基础URL，默认为生产环境
        timeout: 请求超时时间（秒），默认30秒
        max_retries: 最大重试次数，默认3次
        verify_ssl: 是否验证SSL证书，默认True
    
    Example:
        >>> config = SSOConfig(
        ...     client_id="your_client_id",
        ...     client_secret="your_client_secret",
        ...     sso_base_url="https://sso-api.treer.ru"
        ... )
    """
    client_id: str
    client_secret: str
    sso_base_url: str = "https://sso-api.treer.ru"
    timeout: int = 30
    max_retries: int = 3
    verify_ssl: bool = True
    
    def __post_init__(self) -> None:
        """配置验证"""
        if not self.client_id:
            raise SSOConfigError("client_id不能为空")
        if not self.client_secret:
            raise SSOConfigError("client_secret不能为空")
        if not self.sso_base_url:
            raise SSOConfigError("sso_base_url不能为空")
        
        # 确保URL格式正确
        if not self.sso_base_url.startswith(('http://', 'https://')):
            raise SSOConfigError("sso_base_url必须以http://或https://开头")
        
        # 移除末尾的斜杠
        self.sso_base_url = self.sso_base_url.rstrip('/')
        
        # 验证数值参数
        if self.timeout <= 0:
            raise SSOConfigError("timeout必须大于0")
        if self.max_retries < 0:
            raise SSOConfigError("max_retries不能小于0") 