from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("Demo")

@mcp.tool()
# def hybrid_search(q: str) -> int:
def hybrid_search(q = "return") -> int:
    """Search information related to the query.

    Args:
        q: query/question that needs to be queried.

    Returns:
        Information related to the query/question.
    """
    response = requests.get(
        url=f"http://127.0.0.1:8000/hybrid_search/{q}",
        headers={
            "Content-Type": "application/json"
        },
    )

    return response.json()

if __name__ == '__main__':
    mcp.run(transport="stdio")