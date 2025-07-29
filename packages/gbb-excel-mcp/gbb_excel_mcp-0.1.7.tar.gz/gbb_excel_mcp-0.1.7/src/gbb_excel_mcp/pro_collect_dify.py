import requests
import json
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("GbbSearchServer")

#让大模型去修改输入描述，主要是提取商品名称、品牌、型号、参数等
@mcp.tool(name="提取输入关键词",description="根据商品描述，提取商品名称、品牌、型号、参数等")
def difyCollect(pro_name) :
    api_key = "app-rX8oKutNmXaPEms4EUNxmdSs"
    url = 'https://agent-backend-uat.zkh360.com/v1/workflows/run'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "inputs": {"input":pro_name},
        "response_mode": "blocking",
        "user": "abc-123"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        data = json.loads(response.text)
        result = data["data"]["outputs"]["text"]
        print(result)
        return result
    return ""

def run():
    mcp.run(transport="stdio")

if __name__ == "__main__":
   run()

