#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试SSOConfig配置类
"""

import pytest
from treer_sso_sdk import SSOConfig, SSOConfigError


class TestSSOConfig:
    """SSOConfig测试类"""
    
    def test_valid_config(self):
        """测试有效配置"""
        config = SSOConfig(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )
        
        assert config.client_id == "test_client_id"
        assert config.client_secret == "test_client_secret"
        assert config.sso_base_url == "https://sso-api.treer.ru"
        assert config.timeout == 30
        assert config.max_retries == 3
        assert config.verify_ssl is True
    
    def test_custom_config(self):
        """测试自定义配置"""
        config = SSOConfig(
            client_id="test_client_id",
            client_secret="test_client_secret",
            sso_base_url="https://custom.example.com",
            timeout=60,
            max_retries=5,
            verify_ssl=False
        )
        
        assert config.sso_base_url == "https://custom.example.com"
        assert config.timeout == 60
        assert config.max_retries == 5
        assert config.verify_ssl is False
    
    def test_url_normalization(self):
        """测试URL规范化"""
        config = SSOConfig(
            client_id="test_client_id",
            client_secret="test_client_secret",
            sso_base_url="https://example.com/"  # 末尾有斜杠
        )
        
        assert config.sso_base_url == "https://example.com"  # 斜杠被移除
    
    def test_empty_client_id(self):
        """测试空的client_id"""
        with pytest.raises(SSOConfigError, match="client_id不能为空"):
            SSOConfig(
                client_id="",
                client_secret="test_client_secret"
            )
    
    def test_empty_client_secret(self):
        """测试空的client_secret"""
        with pytest.raises(SSOConfigError, match="client_secret不能为空"):
            SSOConfig(
                client_id="test_client_id",
                client_secret=""
            )
    
    def test_empty_sso_base_url(self):
        """测试空的sso_base_url"""
        with pytest.raises(SSOConfigError, match="sso_base_url不能为空"):
            SSOConfig(
                client_id="test_client_id",
                client_secret="test_client_secret",
                sso_base_url=""
            )
    
    def test_invalid_url_scheme(self):
        """测试无效的URL协议"""
        with pytest.raises(SSOConfigError, match="sso_base_url必须以http://或https://开头"):
            SSOConfig(
                client_id="test_client_id",
                client_secret="test_client_secret",
                sso_base_url="ftp://example.com"
            )
    
    def test_invalid_timeout(self):
        """测试无效的超时时间"""
        with pytest.raises(SSOConfigError, match="timeout必须大于0"):
            SSOConfig(
                client_id="test_client_id",
                client_secret="test_client_secret",
                timeout=0
            )
    
    def test_invalid_max_retries(self):
        """测试无效的最大重试次数"""
        with pytest.raises(SSOConfigError, match="max_retries不能小于0"):
            SSOConfig(
                client_id="test_client_id",
                client_secret="test_client_secret",
                max_retries=-1
            ) 