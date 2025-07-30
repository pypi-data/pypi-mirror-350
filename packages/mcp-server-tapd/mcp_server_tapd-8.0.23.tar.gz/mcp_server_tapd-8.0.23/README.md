# TAPD MCP Server

TAPD 是腾讯敏捷研发管理平台，覆盖需求、计划、研发、测试、发布研发全生命周期。支持用自然语言与 TAPD 对话，实现需求、缺陷、任务、迭代等管理。

* 与 TAPD API 无缝集成，提升开发效率

## System requirements

* uv
* TAPD API Token

## Setup Guide
### Install uv
```
brew install uv
# OR
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Get TAPD API Token
Get API tokens from: https://www.tapd.cn/open_platform/open_api_redirect

1. 未注册，请前往 [注册](https://www.tapd.cn?from_partner=copilot&source=tapd_operation_copilot)
2. 已注册但未授权API，请前往API配置：登录TAPD，点击进入[“公司管理-API账号管理”](https://www.tapd.cn/open_platform/open_api_redirect)，复制API账号和API密钥
3. 参数
- TAPD_API_USER: API账号 
- TAPD_API_PASSWORD: API密钥 
- BOT_URL: 企业微信机器人 webhook 地址，选填，如果需要发送消息到企业微信群才需要填


## Configuration and Usage
### Claude Desktop Setup
```
{
  "mcpServers": {
    "mcp-server-tapd": {
      "command": "uvx",
      "args": ["mcp-server-tapd"],
      "env": {
        "TAPD_API_USER": "",
        "TAPD_API_PASSWORD": "",
        "TAPD_API_BASE_URL": "https://api.tapd.cn",
        "TAPD_BASE_URL": "https://www.tapd.cn",
        "BOT_URL": ""
      }
    }
  }
}
```

### Cursor IDE Setup
1. Open Cursor Settings
2. Navigate to Features > MCP Servers
3. Click Add new MCP server

For stdio transport:
```
name: mcp-server-tapd
type: command
command: uvx mcp-server-tapd --api-user=your_api_user --api-password=your_api_password --api-base-url=https://api.tapd.cn --tapd-base-url=https://www.tapd.cn  --bot-url=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=XXX
```

### SSE Transport Configuration
Using SSE Instead of stdio
1. Start the server manually in a terminal:
```
git clone https://cnb.cool/tapd_mcp/mcp-server-tapd.git

cd mcp-server-tapd/src/mcp_server_tapd

uv venv && source .venv/bin/activate

uv pip install requests markdown mcp mcp_server_tapd

python server.py --mode=http --api-user=your_api_user --api-password=your_api_password --api-base-url=https://api.tapd.cn --tapd-base-url=https://www.tapd.cn  --bot-url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=XXX"
```

2. Configure your IDE to connect to the running server via its URL:
```
{
  "mcpServers": {
    "mcp-server-tapd-sse": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```