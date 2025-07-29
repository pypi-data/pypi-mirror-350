#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Treer SSO SDK HTTP客户端实现
"""

import logging
from typing import Optional
import httpx

from .config import SSOConfig
from .interfaces import HTTPClientInterface


class AsyncHTTPClient(HTTPClientInterface):
    """异步HTTP客户端实现
    
    基于httpx库的HTTP客户端，支持连接池和超时控制
    """
    
    def __init__(self, config: SSOConfig) -> None:
        """初始化HTTP客户端
        
        Args:
            config: SSO配置对象
        """
        self.config = config
        self._client: Optional[httpx.AsyncClient] = None
        self.logger = logging.getLogger(__name__)
    
    @property
    def client(self) -> httpx.AsyncClient:
        """懒加载HTTP客户端
        
        Returns:
            httpx.AsyncClient实例
        """
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
                limits=httpx.Limits(
                    max_keepalive_connections=5,
                    max_connections=10
                )
            )
        return self._client
    
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """发送POST请求
        
        Args:
            url: 请求URL
            **kwargs: 请求参数
            
        Returns:
            HTTP响应对象
            
        Raises:
            httpx.RequestError: 网络请求错误
        """
        self.logger.debug(f"发送POST请求: {url}")
        return await self.client.post(url, **kwargs)
    
    async def get(self, url: str, **kwargs) -> httpx.Response:
        """发送GET请求
        
        Args:
            url: 请求URL
            **kwargs: 请求参数
            
        Returns:
            HTTP响应对象
            
        Raises:
            httpx.RequestError: 网络请求错误
        """
        self.logger.debug(f"发送GET请求: {url}")
        return await self.client.get(url, **kwargs)
    
    async def close(self) -> None:
        """关闭连接
        
        清理HTTP客户端资源
        """
        if self._client:
            await self._client.aclose()
            self._client = None
            self.logger.debug("HTTP客户端已关闭") 