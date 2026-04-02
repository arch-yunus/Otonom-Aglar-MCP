import os
from mcp.server.fastmcp import FastMCP

# Modül 2: Yerel Sunucular - Dosya Sistemi Sunucusu
# Bu sunucu bilgisayarınızdaki dosyalara LLM'in güvenli erişimini sağlar.

mcp = FastMCP("Dosya Sistemi Sunucusu")

@mcp.tool()
def list_directory(path: str = ".") -> list[str]:
    """Belirtilen dizindeki dosyaları ve klasörleri listeler."""
    try:
        return os.listdir(path)
    except Exception as e:
        return [f"Hata: {str(e)}"]

@mcp.tool()
def read_file(path: str) -> str:
    """Belirtilen dosyanın içeriğini okur."""
    if not os.path.isfile(path):
        return f"Hata: {path} bir dosya değil."
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Hata: Dosya okunurken sorun oluştu: {str(e)}"

@mcp.tool()
def get_file_stats(path: str) -> dict:
    """Dosya hakkında boyut ve değiştirilme zamanı gibi bilgileri döner."""
    try:
        stats = os.stat(path)
        return {
            "size_bytes": stats.st_size,
            "modified_at": stats.st_mtime,
            "is_directory": os.path.isdir(path)
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("file://{path}")
def file_resource(path: str) -> str:
    """Bir dosyayı salt okunur bir kaynak olarak açar."""
    return read_file(path)

if __name__ == "__main__":
    mcp.run()
