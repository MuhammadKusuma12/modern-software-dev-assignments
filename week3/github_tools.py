import logging
import os
from typing import Any

import requests

logger = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"
DEFAULT_TIMEOUT = 10


def _headers() -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _request_json(url: str, params: dict[str, str] | None = None) -> Any:
    try:
        response = requests.get(
            url,
            params=params,
            headers=_headers(),
            timeout=DEFAULT_TIMEOUT,
        )
    except requests.Timeout:
        logger.exception("GitHub API request timed out")
        raise ValueError(
            f"GitHub API request timed out after {DEFAULT_TIMEOUT} seconds."
        ) from None
    except requests.RequestException as exc:
        logger.exception("GitHub API request failed")
        raise ValueError(f"Failed to reach GitHub API: {exc}") from exc

    remaining = response.headers.get("X-RateLimit-Remaining")
    if response.status_code == 403 and remaining == "0":
        reset = response.headers.get("X-RateLimit-Reset", "unknown")
        logger.warning("GitHub API rate limit exceeded (resets at %s)", reset)
        raise ValueError(
            "GitHub API rate limit exceeded. Set GITHUB_TOKEN for higher limits "
            "and try again later."
        )

    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        logger.exception("GitHub API returned HTTP %s", response.status_code)
        raise ValueError(
            f"GitHub API error: {response.status_code} {response.reason}"
        ) from exc

    return response.json()


def search_repositories(query: str) -> list[dict[str, Any]]:
    query = query.strip()
    if not query:
        raise ValueError("Search query cannot be empty.")

    data = _request_json(
        f"{GITHUB_API}/search/repositories",
        params={"q": query, "per_page": "5"},
    )
    items = data.get("items", [])
    if not items:
        logger.info("No repositories found for query: %s", query)
        return []

    return [
        {"name": repo["full_name"], "stars": repo["stargazers_count"]}
        for repo in items[:5]
    ]


def get_repo_issues(owner: str, repo: str) -> list[dict[str, str]]:
    owner = owner.strip()
    repo = repo.strip()
    if not owner or not repo:
        raise ValueError("Both owner and repo are required.")

    issues = _request_json(
        f"{GITHUB_API}/repos/{owner}/{repo}/issues",
        params={"per_page": "10", "state": "all"},
    )

    if not issues:
        logger.info("No issues found for %s/%s", owner, repo)
        return []

    return [
        {"title": issue["title"], "state": issue["state"]}
        for issue in issues
        if "pull_request" not in issue
    ][:10]
