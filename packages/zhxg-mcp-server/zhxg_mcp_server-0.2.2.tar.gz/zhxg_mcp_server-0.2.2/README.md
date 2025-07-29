# 智慧星光 MCP 服务

由智慧星光提供的互联网开源信息搜索能力，支持布尔逻辑关键词表达式及指定时间范围。

## 功能特点

- 支持布尔运算的关键词搜索，其中布尔运算符（OR、AND）必须使用大写，例如：人工智能 AND 医疗 AND 应用
- 支持时间范围过滤，例如：12h（最近 12 小时）、7d（最近 7 天）等
- 支持自定义返回结果数量，单次不超过 100 条

## 安装

推荐使用 [uv](https://github.com/astral-sh/uv) 或 pip：

```bash
# 使用 uv
uv pip install zhxg-mcp-server

# 或使用 pip
pip install zhxg-mcp-server
```

## 快速开始

### 通过 MCP Inspector 调试

```bash
export ZHXG_API_KEY=<YOUR_API_KEY>
npx -y @modelcontextprotocol/inspector uv run ./src/zhxg_mcp_server/server.py
```

## 环境变量

- `ZHXG_API_KEY`：用于访问智慧星光搜索 API 的密钥，获取方式 [道丁数据平台](https://dowding.istarshine.com)。

### MCP Servers 配置示例

```json
{
  "mcpServers": {
    "zhxg_mcp_server": {
      "command": "uvx",
      "args": [
        "zhxg_mcp_server"
      ],
      "env": {
        "ZHXG_API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

## Cherry Studio 配置

- 在 Cherry Studio 中配置 MCP 服务器时，参数填写示例如下图所示：

<a href="https://dowding.istarshine.com/">
  <img width="480" heigh="320" src="http://dl.istarshine.com/xgsj/cherry_studio.png" alt="ZHXG MCP Server" />
</a>

