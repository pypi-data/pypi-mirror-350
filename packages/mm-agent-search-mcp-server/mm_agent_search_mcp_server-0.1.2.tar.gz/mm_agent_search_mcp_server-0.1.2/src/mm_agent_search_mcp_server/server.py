from mcp.server.fastmcp import FastMCP
import requests
import os

mcp = FastMCP("Demo")

HOST = os.getenv("HOST", "localhost")

@mcp.tool()
def web_search(query: str):
    """Search information from the websites for the query.

    Args:
        query: query that needs to be searched for in the website.

    Returns:
        List of content from the website for the query.
    """
    response = requests.get(
        url=f"http://{HOST}:8001/web_search/{query}",
        headers={
            "Content-Type": "application/json"
        },
    )

    search_results = response.json()["results"]
    results = []
    for search_result in search_results:
        results.append({
            "title": search_result.get("title"),
            "content": search_result.get("content"),
        })

    return results

def main():
    mcp.run(transport="stdio")