# Changelog

所有该项目的重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 计划功能
- 添加刷新令牌支持
- 添加同步API
- 添加更多单元测试

## [1.0.0] - 2024-01-XX

### Added
- 初始版本发布
- OAuth 2.0授权码流程支持
- 异步HTTP客户端基于httpx
- 完整的类型提示
- 用户信息获取功能
- 访问令牌管理
- 详细的异常处理
- Django和Flask集成示例
- 完整的API文档
- 便捷函数支持快速集成

### Features
- `TreerSSOClient` - 主要SSO客户端类
- `SSOConfig` - 配置管理
- `UserInfo` 和 `UserProfile` - 数据模型
- `get_user_info_by_code` - 便捷函数
- 支持自定义HTTP客户端（便于测试）
- 异步上下文管理器支持

### Security
- SSL证书验证默认启用
- 安全的OAuth 2.0实现
- 敏感信息不记录到日志