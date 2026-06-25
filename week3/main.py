import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from github_tools import get_repo_issues, search_repositories

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("GitHub MCP Server")


@mcp.tool()
def search_repos(query: str) -> list[dict[str, Any]]:
    """Search GitHub repositories by keyword and return the top 5 matches."""
    logger.info("search_repos query=%r", query)
    return search_repositories(query)


@mcp.tool()
def repository_issues(owner: str, repo: str) -> list[dict[str, str]]:
    """List up to 10 open or closed issues for a GitHub repository."""
    logger.info("repository_issues owner=%r repo=%r", owner, repo)
    return get_repo_issues(owner, repo)


if __name__ == "__main__":
    mcp.run()
