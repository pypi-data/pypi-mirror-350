# Say Hi MCP Server

[![PyPI version](https://badge.fury.io/py/say-hi-mcp.svg)](https://badge.fury.io/py/say-hi-mcp)
[![Python Support](https://img.shields.io/pypi/pyversions/say-hi-mcp.svg)](https://pypi.org/project/say-hi-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

这是一个简单的 MCP (Model Context Protocol) Server 示例，提供了几个向不同人打招呼的工具。这个项目旨在展示如何创建和部署一个基本的 MCP Server。

## 特性

- 🚀 基于 FastMCP 的简单实现
- 👋 提供多个打招呼工具
- 🛠️ 包含错误处理示例
- 📦 完整的 Python 包结构
- 🔧 易于扩展和自定义

## 安装

### 使用 uvx（推荐）

[uvx](https://docs.astral.sh/uv/guides/tools/) 是运行 Python 包的现代方式，无需全局安装，避免依赖冲突：

```bash
# 直接运行，无需安装
uvx say-hi-mcp

# 或者使用完整的 PyPI 包名
uvx --from say-hi-mcp say-hi-mcp
```

### 从 PyPI 安装

```bash
pip install say-hi-mcp
```

### 从源码安装

```bash
git clone https://github.com/yourusername/say-hi-mcp.git
cd say-hi-mcp
pip install -e .
```

## 使用方法

### 使用 uvx 运行（推荐）

```bash
uvx say-hi-mcp
```

### 作为命令行工具运行

如果已通过 pip 安装：

```bash
say-hi-mcp
```

### 作为 Python 模块运行

```bash
python -m say_hi_mcp.server
```

### 在代码中使用

```python
from say_hi_mcp import SayHiMCPServer

# 创建服务器实例
server = SayHiMCPServer()

# 运行服务器
server.run()
```

## 可用工具

该 MCP Server 提供以下工具：

1. **`hi_alice(my_name)`**: 向 Alice 打招呼
2. **`hi_bob(my_name)`**: 向 Bob 打招呼
3. **`hi_charlie(my_name)`**: 向 Charlie 打招呼（会抛出异常，用于测试错误处理）
4. **`hi_all(my_name)`**: 获取与所有人打招呼的指导

## 配置 Claude Desktop

### 使用 uvx（推荐）

使用 uvx 可以避免全局安装依赖，保持环境整洁：

```json
{
    "mcpServers": {
        "say-hi": {
            "command": "uvx",
            "args": ["say-hi-mcp"]
        }
    }
}
```

**uvx 的优势：**
- ✅ 无需预先安装包
- ✅ 自动管理依赖和虚拟环境
- ✅ 避免依赖冲突
- ✅ 始终使用最新版本（除非指定版本）

### 使用已安装的包

如果你已经通过 pip 安装了包：

```json
{
    "mcpServers": {
        "say-hi": {
            "command": "say-hi-mcp"
        }
    }
}
```

### 使用 Python 直接运行

```json
{
    "mcpServers": {
        "say-hi": {
            "command": "python",
            "args": [
                "-m", "say_hi_mcp.server"
            ]
        }
    }
}
```

### 指定特定版本（uvx）

如果需要使用特定版本：

```json
{
    "mcpServers": {
        "say-hi": {
            "command": "uvx",
            "args": ["--from", "say-hi-mcp==0.1.0", "say-hi-mcp"]
        }
    }
}
```

## 开发

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/yourusername/say-hi-mcp.git
cd say-hi-mcp

# 安装开发依赖
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black say_hi_mcp/
isort say_hi_mcp/
```

### 类型检查

```bash
mypy say_hi_mcp/
```

## 贡献

欢迎贡献！请先 fork 这个仓库，然后创建一个新的分支来进行你的修改。

1. Fork 这个项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

这个项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 相关链接

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [FastMCP 文档](https://github.com/jlowin/fastmcp)
- [Anthropic Claude](https://claude.ai/)
- [uvx 文档](https://docs.astral.sh/uv/guides/tools/)

## 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本历史和更新内容。 