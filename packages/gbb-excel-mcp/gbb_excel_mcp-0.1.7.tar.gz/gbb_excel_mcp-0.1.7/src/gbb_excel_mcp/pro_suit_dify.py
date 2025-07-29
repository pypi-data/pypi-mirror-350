
import requests
import json
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("GbbSearchServer")
#让大模型去匹配商品
@mcp.tool(name="商品匹配",description="根据商品描述，从商品列表中找出满足商品描述的商品")
def difySuit(pro_name:str,pro_list:list) :
    api_key = "app-ibRumVO3acor0yb9EH35YSC2"
    url = 'https://agent-backend-uat.zkh360.com/v1/workflows/run'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    print(type(pro_list))
    data = {
        "inputs": {"pro_name":pro_name,"pro_list":json.dumps(pro_list)},
        "response_mode": "blocking",
        "user": "abc-123"
    }
    response = requests.post(url, headers=headers, json=data)
    print("resonse:")
    print(response.text)
    if response.status_code == 200:
        data = json.loads(response.text)
        print(data)
        result = data["data"]["outputs"]["result"]
        temp = json.loads(result)
        skuNo = temp["skuNo"]
        print(skuNo)
        return skuNo
    return ""

def run():
    mcp.run(transport="stdio")

if __name__ == "__main__":
   run()
