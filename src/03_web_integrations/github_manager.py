import os
from github import Github
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Modül 3: Dış Dünya Entegrasyonları - GitHub Yöneticisi
# Bu sunucu LLM'in GitHub üzerindeki depoları analiz etmesini sağlar.

load_dotenv()
mcp = FastMCP("GitHub Yöneticisi")

# GITHUB_TOKEN gereklidir
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_github_client():
    if not GITHUB_TOKEN:
        raise ValueError("Lütfen GITHUB_TOKEN çevre değişkenini ayarlayın.")
    return Github(GITHUB_TOKEN)

@mcp.tool()
def get_repo_details(repo_name: str) -> dict:
    """
    Belirtilen GitHub deposu (Repo) hakkında detaylı bilgi döner.
    Örn repo_name: 'bahattinyunus/Otonom-Aglar-MCP'
    """
    try:
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
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_repo_issues(repo_name: str, state: str = "open") -> list[dict]:
    """Depodaki issue'ları listeler."""
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        issues = []
        for issue in repo.get_issues(state=state):
            issues.append({
                "number": issue.number,
                "title": issue.title,
                "user": issue.user.login,
                "labels": [label.name for label in issue.labels]
            })
            if len(issues) >= 10: break # Örnek için sınırla
        return issues
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def read_github_file(repo_name: str, file_path: str) -> str:
    """GitHub üzerindeki bir dosyanın içeriğini okur."""
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        contents = repo.get_contents(file_path)
        return contents.decoded_content.decode()
    except Exception as e:
        return f"Hata: Dosya okunamadı: {str(e)}"

if __name__ == "__main__":
    mcp.run()
