from mcp.server.fastmcp import FastMCP
import aiohttp
import os

mcp = FastMCP("Demo")

host = os.getenv("host", "localhost")

@mcp.tool()
async def hybrid_search(query: str) -> int:
    """Search information related to the query.

    Args:
        query: query/key word that needs to be queried.

    Returns:
        Information related to the query/question.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{host}:8000/hybrid_search/{query}") as response:
            print(response.status)
            data = await response.json()
            print(data)
            return data

def main():
    mcp.run(transport="stdio")