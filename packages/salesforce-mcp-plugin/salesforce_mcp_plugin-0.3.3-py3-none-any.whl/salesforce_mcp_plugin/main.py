from mcp.server.fastmcp import FastMCP
from salesforce_mcp_plugin.salesforce import query_accounts

mcp = FastMCP("salesforce-query")

@mcp.tool()
async def search_account_by_name(token: str, instance_url: str, name: str) -> str:
    """根据客户名称查询 Salesforce 中的 Account 数据。

    Args:
        token: Salesforce 的访问令牌（access token）
        instance_url: Salesforce 实例的 URL（例如 https://your-instance.salesforce.com）
        name: 客户名称的一部分
    """
    accounts = query_accounts(token, instance_url, name)

    if not accounts:
        return f"没有找到名称包含“{name}”的客户记录。"

    return "\n".join(accounts)

def main():
    print("FastMCP is starting...")
    mcp.run(transport='stdio')