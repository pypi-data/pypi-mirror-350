#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Treer SSO SDK异常定义
"""

from typing import Optional, Dict, Any


class SSOError(Exception):
    """SSO SDK基础异常"""
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None, 
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message='{self.message}', "
            f"error_code='{self.error_code}', "
            f"details={self.details})"
        )


class SSOConfigError(SSOError):
    """SSO配置错误"""
    pass


class SSOAuthenticationError(SSOError):
    """SSO认证错误"""
    pass


class SSONetworkError(SSOError):
    """SSO网络错误"""
    pass


class SSOInvalidTokenError(SSOAuthenticationError):
    """无效的访问令牌"""
    pass


class SSOInvalidCodeError(SSOAuthenticationError):
    """无效的授权码"""
    pass 