import os
import sys
import asyncio
import base64
from typing import Dict, Any, Optional

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.utils import create_mcp_server, setup_logging, tool_error_handler

# Modül 3: Dış Dünya Entegrasyonları - Gelişmiş Web Kazıyıcı (Playwright)
# Bu sunucu LLM'in JavaScript ağır siteleri ("Single Page App") render etmesini
# ve sayfa ekran görüntülerini yakalamasını sağlar.

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright SDK bulunamadı. Lütfen 'pip install playwright' ve 'playwright install' adımlarını izleyin.")

setup_logging()
mcp = create_mcp_server("Playwright Gelişmiş Web Sunucusu")

@mcp.tool()
@tool_error_handler
async def render_js_page(url: str, wait_time: int = 2) -> str:
    """
    Modern web sayfalarını (React, Vue, vb.) tarayıcıda render eder ve içeriğini döner.
    Basit kazıyıcıların (httpx) göremediği dinamik içerikleri görmek için kullanılır.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        
        # Ekstra bekleme Paywright'in render işlemini bitirmesi için
        await asyncio.sleep(wait_time)
        
        content = await page.content()
        await browser.close()
        
        # Basitlik için ham HTML döner (Modül 3 scraper ile birleştirilebilir)
        return content[:20000] # Token sınırı kontrolü

@mcp.tool()
@tool_error_handler
async def take_screenshot(url: str, filename: Optional[str] = None) -> str:
    """
    Belirtilen URL'nin tam sayfa ekran görüntüsünü alır. 
    Özellikle görsel tasarım ve UI analizi bekleyen LLM modelleri için kritiktir.
    """
    if not filename:
        filename = f"screenshot_{int(asyncio.get_event_loop().time())}.png"
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        
        # Dizin kontrolü
        os.makedirs("screenshots", exist_ok=True)
        path = os.path.join("screenshots", filename)
        
        await page.screenshot(path=path, full_page=True)
        await browser.close()
        
    return f"BAŞARILI: Ekran görüntüsü '{path}' adresine kaydedildi."

if __name__ == "__main__":
    mcp.run()
