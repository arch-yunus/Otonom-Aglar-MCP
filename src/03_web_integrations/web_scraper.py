import httpx
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
import os

# Modül 3: Dış Dünya Entegrasyonları - Web Scraper
# Bu sunucu LLM'in internetteki içerikleri okumasına ve analiz etmesine olanak tanır.

mcp = FastMCP("Otonom Web Scraper")

# Çevre değişkenlerinden ayarları yükle
USER_AGENT = os.getenv("USER_AGENT", "Otonom-Aglar-MCP/1.0")
TIMEOUT = int(os.getenv("SCRAPE_TIMEOUT", "15"))

@mcp.tool()
def scrape_url(url: str) -> str:
    """
    Belirtilen URL'deki içeriği HTML'den arındırıp temiz metin olarak döner.
    LLM'lerin web sayfalarını anlaması için optimize edilmiştir.
    """
    try:
        headers = {"User-Agent": USER_AGENT}
        with httpx.Client(headers=headers, timeout=TIMEOUT) as client:
            response = client.get(url)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Gereksiz etiketleri temizle
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
            
        # Metni al ve temizle
        text = soup.get_text(separator='\n')
        lines = (line.strip() for line in text.splitlines())
        clean_text = '\n'.join(line for line in lines if line)
        
        # Çok uzun içerikleri sınırla (Token tasarrufu)
        return clean_text[:8000] 
    except Exception as e:
        return f"Hata: URL kazınırken sorun oluştu: {str(e)}"

@mcp.tool()
def extract_links(url: str) -> list[str]:
    """Sayfadaki tüm dış bağlantıları (URL) çıkarır."""
    try:
        headers = {"User-Agent": USER_AGENT}
        with httpx.Client(headers=headers, timeout=TIMEOUT) as client:
            response = client.get(url)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.append(href)
        return list(set(links)) # Benzersiz olanları dön
    except Exception as e:
        return [f"Hata: Bağlantılar alınamadı: {str(e)}"]

if __name__ == "__main__":
    mcp.run()
