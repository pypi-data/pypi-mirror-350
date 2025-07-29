from typing import Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("tl_mcp_server")

@mcp.tool(description="将自定义的图片或者文案推送微信社群")
def promote(send_content: str, send_image_url) -> str:
    return "自定义内容已推送，请[点击链接](https://baidu.com/)查看推送详情" 

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
