# Treer SSO SDK

[![PyPI version](https://badge.fury.io/py/treer-sso-sdk.svg)](https://badge.fury.io/py/treer-sso-sdk)
[![Python Support](https://img.shields.io/pypi/pyversions/treer-sso-sdk.svg)](https://pypi.org/project/treer-sso-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/treer-ru/treer-sso-sdk/workflows/测试/badge.svg)](https://github.com/treer-ru/treer-sso-sdk/actions)
[![codecov](https://codecov.io/gh/treer-ru/treer-sso-sdk/branch/main/graph/badge.svg)](https://codecov.io/gh/treer-ru/treer-sso-sdk)

> 🚀 用于快速集成Treer SSO服务的Python SDK，支持OAuth 2.0授权码流程

## ✨ 特性

- 🔐 **OAuth 2.0支持**: 完整的授权码流程实现
- ⚡ **异步支持**: 基于httpx的高性能异步HTTP客户端  
- 🛡️ **类型安全**: 完整的类型提示支持
- 🔧 **易于集成**: 提供便捷函数和高级客户端类
- 📖 **完整文档**: 详细的API文档和使用示例
- 🧪 **测试覆盖**: 高质量的单元测试
- 🐍 **现代Python**: 支持Python 3.11+

## 🚀 快速开始

### 安装

```bash
pip install treer-sso-sdk
```

### 基础使用

```python
import asyncio
from treer_sso_sdk import get_user_info_by_code

async def main():
    user_info = await get_user_info_by_code(
        authorization_code="your_auth_code",
        client_id="your_client_id", 
        client_secret="your_client_secret"
    )
    
    print(f"用户: {user_info.username}")
    print(f"邮箱: {user_info.email}")

asyncio.run(main())
```

### 高级使用

```python
import asyncio
from treer_sso_sdk import TreerSSOClient, SSOConfig

async def main():
    config = SSOConfig(
        client_id="your_client_id",
        client_secret="your_client_secret",
        sso_base_url="https://sso-api.treer.ru"
    )
    
    async with TreerSSOClient(config) as client:
        # 获取访问令牌
        token_response = await client.get_access_token("auth_code")
        
        # 获取用户信息
        user_info = await client.get_user_info(token_response.access_token)
        
        print(f"用户ID: {user_info.id}")
        print(f"用户名: {user_info.username}")

asyncio.run(main())
```

## 📚 文档

- [GitHub发布指南](GITHUB_RELEASE.md)
- [变更日志](CHANGELOG.md)
- [许可证](LICENSE)

## 🔧 开发

### 本地开发设置

```bash
# 克隆仓库
git clone https://github.com/treer-ru/treer-sso-sdk.git
cd treer-sso-sdk

# 安装开发依赖
pip install -e .[dev]

# 运行测试
pytest tests/

# 代码格式化
black src/
isort src/

# 类型检查  
mypy src/treer_sso_sdk/
```

### 构建和发布

```bash
# 使用构建脚本
python scripts/build.py all

# 或手动构建
python -m build
twine check dist/*
```

## 🤝 贡献

欢迎贡献代码！

### 开发流程

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🔗 相关链接

- [PyPI](https://pypi.org/project/treer-sso-sdk/)
- [GitHub](https://github.com/treer-ru/treer-sso-sdk)
- [问题反馈](https://github.com/treer-ru/treer-sso-sdk/issues)
- [变更日志](CHANGELOG.md)

## 💬 支持

如果您遇到问题或有疑问：

- 📋 [提交Issue](https://github.com/treer-ru/treer-sso-sdk/issues)
- 📧 发送邮件至: dev@treer.ru

---

⭐ 如果这个项目对您有帮助，请给我们一个star！