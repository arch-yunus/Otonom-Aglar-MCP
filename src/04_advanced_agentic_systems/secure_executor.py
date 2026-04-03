import os
import sys
from pathlib import Path

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.utils import create_mcp_server, setup_logging, tool_error_handler

# Modül 4: İleri Seviye Sistemler - Güvenli Korumalı Alan (Sandbox) Sunucusu
setup_logging()
mcp = create_mcp_server("Güvenli Korumalı Alan (Sandbox)")

# Sadece bu dizin içinde işlem yapılabilir (Sandbox Root)
# Güvenlik için ortam değişkeninden alınır, yoksa güvenli temp kullanılır.
SANDBOX_DIR = os.getenv("MCP_SANDBOX_DIR", os.path.join(os.getcwd(), "mcp_sandbox"))

def is_safe_path(requested_path: str) -> bool:
    """Path Traversal (Dizin Atlama) saldırılarını engeller."""
    # Güvenlik Kontrolü 1: İstenen yolu sandox'ın mutlak yoluna bağla
    base = Path(SANDBOX_DIR).resolve()
    # Güvenlik Kontrolü 2: Hedef yolu çöz (../../ gibi atlamaları çözer)
    target = Path(os.path.join(SANDBOX_DIR, requested_path)).resolve()
    
    # Güvenlik Kontrolü 3: Hedef yol, base yolun altında mı?
    try:
        target.relative_to(base)
        return True
    except ValueError:
        return False

@mcp.tool()
@tool_error_handler
def init_sandbox() -> str:
    """Korumalı alanı (Sandbox) başlatır ve dizini oluşturur."""
    os.makedirs(SANDBOX_DIR, exist_ok=True)
    return f"Sandbox hazırlandı: {SANDBOX_DIR}. Artık güvenle dosya yazabilirsiniz."

@mcp.tool()
@tool_error_handler
def secure_write_file(filename: str, content: str) -> str:
    """
    SADECE korumalı alan içine (Sandbox) dosya yazar. 
    Kritik sistem dosyaları değiştirilemez.
    """
    if not is_safe_path(filename):
        return "GÜVENLİK İHLALİ (Path Traversal): Sandbox dışına yazamazsınız!"
    
    target_path = Path(SANDBOX_DIR) / filename
    # Alt dizinler gerekiyorsa oluştur
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"BAŞARILI: {filename} sandbox içine güvenle kaydedildi."

@mcp.tool()
@tool_error_handler
def secure_read_file(filename: str) -> str:
    """SADECE korumalı alan içindeki (Sandbox) dosyaları okur."""
    if not is_safe_path(filename):
        return "GÜVENLİK İHLALİ: Sandbox dışını okuyamazsınız!"
    
    target_path = Path(SANDBOX_DIR) / filename
    if not target_path.exists():
        return f"HATA: Dosya bulunamadı: {filename}"
        
    with open(target_path, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
@tool_error_handler
def secure_list_sandbox() -> list[str]:
    """Sandbox (Korumalı alan) içindeki dosyaları listeler."""
    if not os.path.exists(SANDBOX_DIR):
         os.makedirs(SANDBOX_DIR, exist_ok=True)
    return os.listdir(SANDBOX_DIR)

if __name__ == "__main__":
    mcp.run()
