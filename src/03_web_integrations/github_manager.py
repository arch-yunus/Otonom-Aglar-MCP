import os
import sys
from github import Github
from dotenv import load_dotenv

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.utils import create_mcp_server, setup_logging, tool_error_handler

load_dotenv()
setup_logging()
mcp = create_mcp_server("GitHub Yöneticisi")

# GITHUB_TOKEN gereklidir
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_github_client():
    if not GITHUB_TOKEN:
        raise ValueError("Lütfen GITHUB_TOKEN çevre değişkenini ayarlayın.")
    return Github(GITHUB_TOKEN)

@mcp.tool()
@tool_error_handler
def get_repo_details(repo_name: str) -> dict:
    """
    Belirtilen GitHub deposu (Repo) hakkında detaylı bilgi döner.
    Örn repo_name: 'bahattinyunus/Otonom-Aglar-MCP'
    """
    g = get_github_client()
    repo = g.get_repo(repo_name)
    return {
        "full_name": repo.full_name,
        "description": repo.description,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "open_issues": repo.open_issues_count,
        "language": repo.language,
        "default_branch": repo.default_branch
    }

@mcp.tool()
@tool_error_handler
def list_repo_issues(repo_name: str, state: str = "open") -> list[dict]:
    """Depodaki issue'ları listeler."""
    g = get_github_client()
    repo = g.get_repo(repo_name)
    issues = []
    # limit to 20 for token safety
    for issue in repo.get_issues(state=state)[:20]:
        issues.append({
            "number": issue.number,
            "title": issue.title,
            "user": issue.user.login,
            "labels": [label.name for label in issue.labels],
            "state": issue.state
        })
    return issues

@mcp.tool()
@tool_error_handler
def read_github_file(repo_name: str, file_path: str) -> str:
    """GitHub üzerindeki bir dosyanın içeriğini okur."""
    g = get_github_client()
    repo = g.get_repo(repo_name)
    contents = repo.get_contents(file_path)
    return contents.decoded_content.decode()

@mcp.tool()
@tool_error_handler
def create_issue(repo_name: str, title: str, body: str) -> dict:
    """Belirtilen depoda yeni bir issue açar."""
    g = get_github_client()
    repo = g.get_repo(repo_name)
    issue = repo.create_issue(title=title, body=body)
    return {"number": issue.number, "url": issue.html_url}

if __name__ == "__main__":
    mcp.run()
