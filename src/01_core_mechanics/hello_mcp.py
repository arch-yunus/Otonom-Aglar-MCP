import sys
import os

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.utils import create_mcp_server, setup_logging, tool_error_handler

# Modül 1: Temeller ve Protokol Mekaniği
setup_logging()
mcp = create_mcp_server("Öğrenci Dostu MCP Sunucusu")

@mcp.tool()
@tool_error_handler
def to_upper(text: str) -> str:
    """Metni büyük harfe çevirir. Protokol testi için basit bir araç."""
    return text.upper()

@mcp.tool()
@tool_error_handler
def echo(message: str) -> str:
    """Gelen mesajı geri döndürür. İletişim testi için kullanılır."""
    return f"Sunucu yanıtı: {message}"

@mcp.resource("mcp://info")
def get_info() -> str:
    """Protokol hakkında bilgi veren statik bir kaynak."""
    return """
    Model Context Protocol (MCP) Bilgi Kartı:
    - Host: Claude Desktop, Cursor, vb.
    - Client: Protokolü yöneten katman.
    - Server: Dış dünyaya açılan kapı (Bu dosya).
    """

@mcp.prompt("analyze-code")
def analyze_code_prompt(code: str) -> str:
    """Kod analizi için optimize edilmiş bir istem şablonu."""
    return f"Aşağıdaki kodu Model Context Protocol perspektifinden analiz et:\n\n{code}"

if __name__ == "__main__":
    mcp.run()
