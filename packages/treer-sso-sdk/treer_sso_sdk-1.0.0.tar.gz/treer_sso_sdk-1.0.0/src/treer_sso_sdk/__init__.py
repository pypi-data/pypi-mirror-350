#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Treer SSO SDK

用于通过OAuth 2.0授权码流程获取用户信息的SDK
支持点餐系统等第三方应用快速集成SSO服务
"""

__version__ = "1.0.0"
__author__ = "Treer Team"
__email__ = "dev@treer.ru"
__license__ = "MIT"

# 导入主要类和函数
from .client import TreerSSOClient
from .config import SSOConfig
from .models import UserInfo, UserProfile, TokenResponse
from .exceptions import (
    SSOError,
    SSOConfigError,
    SSOAuthenticationError,
    SSONetworkError,
    SSOInvalidTokenError,
    SSOInvalidCodeError,
)
from .utils import get_user_info_by_code

# 定义公共API
__all__ = [
    # 版本信息
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    # 主要类
    "TreerSSOClient",
    "SSOConfig",
    # 数据模型
    "UserInfo",
    "UserProfile", 
    "TokenResponse",
    # 异常类
    "SSOError",
    "SSOConfigError",
    "SSOAuthenticationError",
    "SSONetworkError",
    "SSOInvalidTokenError",
    "SSOInvalidCodeError",
    # 便捷函数
    "get_user_info_by_code",
] 