import os
import sys

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.utils import create_mcp_server, setup_logging, tool_error_handler

# Modül 2: Yerel Sunucular - Dosya Sistemi Sunucusu
setup_logging()
mcp = create_mcp_server("Dosya Sistemi Sunucusu")

@mcp.tool()
@tool_error_handler
def list_directory(path: str = ".") -> list[str]:
    """Belirtilen dizindeki dosyaları ve klasörleri listeler."""
    return os.listdir(path)

@mcp.tool()
@tool_error_handler
def read_file(path: str) -> str:
    """Belirtilen dosyanın içeriğini okur."""
    if not os.path.isfile(path):
        return f"Hata: {path} bir dosya değil."
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
@tool_error_handler
def get_file_stats(path: str) -> dict:
    """Dosya hakkında boyut ve değiştirilme zamanı gibi bilgileri döner."""
    stats = os.stat(path)
    return {
        "size_bytes": stats.st_size,
        "modified_at": stats.st_mtime,
        "is_directory": os.path.isdir(path)
    }

@mcp.resource("file://{path}")
def file_resource(path: str) -> str:
    """Bir dosyayı salt okunur bir kaynak olarak açar."""
    return read_file(path)

if __name__ == "__main__":
    mcp.run()
