import httpx
import os
import sys
from bs4 import BeautifulSoup

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.utils import create_mcp_server, setup_logging, tool_error_handler

try:
    from markdownify import markdownify as md
except ImportError:
    # Fallback to simple text if markdownify is not installed
    def md(html, **kwargs):
        return html

# Modül 3: Dış Dünya Entegrasyonları - Web Scraper
setup_logging()
mcp = create_mcp_server("Otonom Web Scraper")

# Çevre değişkenlerinden ayarları yükle
USER_AGENT = os.getenv("USER_AGENT", "Otonom-Aglar-MCP/1.0")
TIMEOUT = int(os.getenv("SCRAPE_TIMEOUT", "15"))

@mcp.tool()
@tool_error_handler
def scrape_url(url: str) -> str:
    """
    Belirtilen URL'deki içeriği HTML'den arındırıp temiz Markdown olarak döner.
    LLM'lerin web sayfalarını anlaması için optimize edilmiştir.
    """
    headers = {"User-Agent": USER_AGENT}
    with httpx.Client(headers=headers, timeout=TIMEOUT, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Gereksiz etiketleri temizle
    for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
        element.decompose()
        
    # Markdown'a çevir
    markdown_content = md(str(soup), heading_style="ATX", strip=["a", "img"])
    
    # Fazla boşlukları temizle
    clean_text = "\n".join([line.strip() for line in markdown_content.splitlines() if line.strip()])
    
    # Token tasarrufu için sınırla
    return clean_text[:12000]

@mcp.tool()
@tool_error_handler
def extract_links(url: str) -> list[str]:
    """Sayfadaki tüm dış bağlantıları (URL) çıkarır."""
    headers = {"User-Agent": USER_AGENT}
    with httpx.Client(headers=headers, timeout=TIMEOUT, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('http'):
            links.append(href)
    return list(set(links))

if __name__ == "__main__":
    mcp.run()
