from mcp.server.fastmcp import FastMCP

# Modül 1: Temeller ve Protokol Mekaniği
# Bu sunucu MCP'nin temel yapı taşlarını (Tools, Resources, Prompts) gösterir.

mcp = FastMCP("Öğrenci Dostu MCP Sunucusu")

@mcp.tool()
def to_upper(text: str) -> str:
    """Metni büyük harfe çevirir. Protokol testi için basit bir araç."""
    return text.upper()

@mcp.tool()
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
