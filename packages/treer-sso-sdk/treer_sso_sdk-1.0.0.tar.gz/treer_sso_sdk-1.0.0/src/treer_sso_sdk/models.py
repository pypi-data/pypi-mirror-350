#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Treer SSO SDK数据模型
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class UserProfile:
    """用户档案信息
    
    Attributes:
        first_name: 名字
        last_name: 姓氏
        avatar_url: 头像URL
        locale: 语言设置，默认为中文
        timezone: 时区设置，默认为上海时区
        additional_info: 附加信息字典
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    locale: str = "zh"
    timezone: str = "Asia/Shanghai"
    additional_info: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def full_name(self) -> str:
        """获取完整姓名"""
        names = [name for name in [self.first_name, self.last_name] if name]
        return " ".join(names) if names else ""


@dataclass
class UserInfo:
    """用户信息数据类
    
    Attributes:
        id: 用户唯一标识符
        username: 用户名
        email: 邮箱地址
        phone: 电话号码
        is_active: 用户是否激活状态
        profile: 用户档案信息
        created_at: 创建时间
        updated_at: 更新时间
    """
    id: str
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    profile: Optional[UserProfile] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserInfo':
        """从字典创建UserInfo实例
        
        Args:
            data: 包含用户信息的字典
            
        Returns:
            UserInfo实例
        
        Raises:
            KeyError: 缺少必需的字段
            ValueError: 数据格式错误
        """
        # 验证必需字段
        if 'id' not in data:
            raise KeyError("缺少必需字段: id")
        if 'username' not in data:
            raise KeyError("缺少必需字段: username")
        
        # 解析用户档案
        profile_data = data.get('profile')
        profile = None
        if profile_data:
            profile = UserProfile(
                first_name=profile_data.get('first_name'),
                last_name=profile_data.get('last_name'),
                avatar_url=profile_data.get('avatar_url'),
                locale=profile_data.get('locale', 'zh'),
                timezone=profile_data.get('timezone', 'Asia/Shanghai'),
                additional_info=profile_data.get('additional_info', {})
            )
        
        # 解析日期时间字段
        created_at = None
        updated_at = None
        
        if data.get('created_at'):
            try:
                created_at = datetime.fromisoformat(
                    data['created_at'].replace('Z', '+00:00')
                )
            except (ValueError, AttributeError):
                # 如果日期格式解析失败，忽略该字段
                pass
        
        if data.get('updated_at'):
            try:
                updated_at = datetime.fromisoformat(
                    data['updated_at'].replace('Z', '+00:00')
                )
            except (ValueError, AttributeError):
                # 如果日期格式解析失败，忽略该字段
                pass
        
        return cls(
            id=str(data['id']),
            username=data['username'],
            email=data.get('email'),
            phone=data.get('phone'),
            is_active=data.get('is_active', True),
            profile=profile,
            created_at=created_at,
            updated_at=updated_at
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """将UserInfo实例转换为字典
        
        Returns:
            包含用户信息的字典
        """
        result = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'is_active': self.is_active,
        }
        
        if self.profile:
            result['profile'] = {
                'first_name': self.profile.first_name,
                'last_name': self.profile.last_name,
                'avatar_url': self.profile.avatar_url,
                'locale': self.profile.locale,
                'timezone': self.profile.timezone,
                'additional_info': self.profile.additional_info,
            }
        
        if self.created_at:
            result['created_at'] = self.created_at.isoformat()
        
        if self.updated_at:
            result['updated_at'] = self.updated_at.isoformat()
        
        return result


@dataclass
class TokenResponse:
    """访问令牌响应
    
    Attributes:
        access_token: 访问令牌
        token_type: 令牌类型，通常为"Bearer"
        expires_in: 令牌有效期（秒）
        refresh_token: 刷新令牌（可选）
        scope: 令牌授权范围（可选）
    """
    access_token: str
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    
    @property
    def authorization_header(self) -> str:
        """获取Authorization头部值"""
        return f"{self.token_type} {self.access_token}" 