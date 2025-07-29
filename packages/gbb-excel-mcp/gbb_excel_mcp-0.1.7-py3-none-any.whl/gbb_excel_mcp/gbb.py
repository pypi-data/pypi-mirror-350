import requests
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("GbbSearchServer")
# 搜索技术
@mcp.tool(name="工邦邦搜索",description="根据输入关键词，去工邦邦官网搜索相关商品")
def search(keyword: str):
    BASE_URL = "https://www.gongbangbang.com"
    url = f"{BASE_URL}/api/gateway/website/gbb/search/product/v2"
    data = {
        "keyword": keyword,
        "channel": 1,
        "clp": False,
        "fz": False,
        "from": 0,
        "size": 20,
        "sort": 0,
    }
    try: 
        response = requests.post(url, headers={"platform": "web"},json=data)
        response.raise_for_status()  # 检查 HTTP 响应的错误
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
