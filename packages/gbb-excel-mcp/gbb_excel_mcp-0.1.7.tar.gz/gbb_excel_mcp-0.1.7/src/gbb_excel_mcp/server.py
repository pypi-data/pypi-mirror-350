from gbb_excel_mcp.gbb import search
from gbb_excel_mcp.pro_suit_dify import difySuit
from gbb_excel_mcp.pro_collect_dify import difyCollect
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("GbbSearchServer")

#匹配商品
@mcp.tool(name="工邦邦商品查询",description="根据商品描述，找出满足条件的商品编码")
def suitProWithKey(key:str) :
    """
    工邦邦商品查询工具
    
    根据用户输入的商品描述关键词，查询匹配的商品编码。流程如下：
    1. 使用关键词调用工邦邦搜索获取商品列表
    2. 从搜索结果中匹配最符合的商品编码
    3. 若无匹配结果，则提取新关键词重新搜索匹配
    
    Args:
        key (str): 商品描述关键词
    
    Returns:
        dict: 包含匹配商品编码的字典，格式为 {"skuNo": "商品编码"}
    """
    print("key:"+key)
    # step1 先根据用户输入去调用工邦邦搜索，获取搜索列表
    search_list = search(key)
    # step2 再用用户输入的关键字，从搜索列表中找到满足需求的商品
    skuNo = difySuit(key,search_list)
    # step3 如果没有匹配的商品，即skuNo==“”
    if skuNo == "" :
        # step3.1 修改用户输入，提取关键字
        newKey = difyCollect(key)
        # step3.2 将新的关键字重新去工邦邦搜索
        new_search_list = search(newKey)
        # step 3.3 将新的关键字跟搜索结果去匹配
        skuNo =  difySuit(newKey,search_list)
    return {"skuNo":skuNo}

def run():
    mcp.run(transport="stdio")


if __name__ == "__main__":
   run()
