# GitHub MCP Server

MCP server lokal (STDIO) yang membungkus [GitHub REST API](https://docs.github.com/en/rest). Menyediakan dua tool untuk mencari repository dan melihat issue.

## Prerequisites

- Python 3.10+
- Akses internet ke `api.github.com`
- (Opsional) [GitHub personal access token](https://github.com/settings/tokens) untuk rate limit lebih tinggi

## Setup

```bash
cd week3
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | No | GitHub PAT. Tanpa token: ~60 request/jam. Dengan token: ~5.000 request/jam. |

Contoh:

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

## Run locally

STDIO transport (default untuk MCP client):

```bash
python main.py
```

Server menulis log ke **stderr** agar tidak mengganggu protokol STDIO.

## Configure Cursor

Tambahkan ke `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "github-mcp": {
      "command": "/path/to/modern-software-dev-assignments/week3/.venv/bin/python",
      "args": [
        "/path/to/modern-software-dev-assignments/week3/main.py"
      ],
      "cwd": "/path/to/modern-software-dev-assignments/week3",
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

Ganti `/path/to/...` dengan path absolut di mesin Anda. Restart Cursor atau reload MCP server di **Settings → MCP**.

## Configure Claude Desktop

Tambahkan ke `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "github-mcp": {
      "command": "/path/to/modern-software-dev-assignments/week3/.venv/bin/python",
      "args": [
        "/path/to/modern-software-dev-assignments/week3/main.py"
      ],
      "cwd": "/path/to/modern-software-dev-assignments/week3"
    }
  }
}
```

Lokasi file config Claude Desktop:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

## Example usage in a client

Setelah server terhubung, minta agent:

- *"Search GitHub repos for fastapi"* → memanggil `search_repos`
- *"Show issues for fastapi/fastapi"* → memanggil `repository_issues`

## Tools

### `search_repos`

Mencari repository GitHub dan mengembalikan 5 hasil teratas.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `query` | string | Kata kunci pencarian (wajib, tidak boleh kosong) |

**Example input**

```json
{ "query": "fastapi" }
```

**Example output**

```json
[
  { "name": "fastapi/fastapi", "stars": 99607 },
  { "name": "fastapi/full-stack-fastapi-template", "stars": 43859 }
]
```

**Behavior**

- Mengembalikan `[]` jika tidak ada hasil
- Error jika query kosong, timeout, HTTP error, atau rate limit tercapai

### `repository_issues`

Mengembalikan hingga 10 issue (bukan pull request) dari repository.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| `owner` | string | Pemilik repo, mis. `fastapi` |
| `repo` | string | Nama repo, mis. `fastapi` |

**Example input**

```json
{ "owner": "fastapi", "repo": "fastapi" }
```

**Example output**

```json
[
  { "title": "Fix docs typo", "state": "open" },
  { "title": "Add validation", "state": "closed" }
]
```

**Behavior**

- Pull request difilter (GitHub API mencampur PR ke endpoint `/issues`)
- Mengembalikan `[]` jika tidak ada issue
- Error jika `owner`/`repo` kosong, repo tidak ditemukan, timeout, atau rate limit

## Error handling

Server menangani:

- **Timeout** (10 detik) — pesan error jelas ke client
- **HTTP errors** (404, 401, dll.) — status code dan reason
- **Rate limit** — peringatan jika `X-RateLimit-Remaining` habis; disarankan set `GITHUB_TOKEN`
- **Input kosong** — validasi sebelum memanggil API
- **Hasil kosong** — mengembalikan list kosong, bukan error

Log operasi ditulis ke stderr via modul `logging`.

## GitHub API endpoints used

| Tool | Endpoint |
|------|----------|
| `search_repos` | `GET /search/repositories` |
| `repository_issues` | `GET /repos/{owner}/{repo}/issues` |

## Project structure

```
week3/
├── main.py           # MCP server entrypoint (FastMCP + tools)
├── github_tools.py   # GitHub API client with error handling
├── requirements.txt
└── README.md
```
