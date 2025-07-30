from mcp.server.fastmcp import FastMCP
import aiohttp

mcp = FastMCP("Demo")

@mcp.tool()
# def hybrid_search(q: str) -> int:
async def hybrid_search(q = "return") -> int:
    """Search information related to the query.

    Args:
        q: query/question that needs to be queried.

    Returns:
        Information related to the query/question.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://127.0.0.1:8000/hybrid_search/{q}") as response:
            print(response.status)
            data = await response.json()
            print(data)
            return data

def main():
    mcp.run(transport="stdio")