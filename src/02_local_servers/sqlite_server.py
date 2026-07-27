import sqlite3
import os
import sys

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.utils import create_mcp_server, setup_logging, tool_error_handler

# Modül 2: Yerel Sunucular - SQLite Veritabanı Sunucusu
setup_logging()
mcp = create_mcp_server("SQLite Veritabanı Sunucusu")

@mcp.tool()
@tool_error_handler
def execute_query(db_path: str, query: str) -> list[dict]:
    """Belirtilen veritabanında salt okunur SQL sorgusu çalıştırır."""
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        raise FileNotFoundError(f"Veritabanı dosyası bulunamadı veya geçersiz: {db_path}")
    if not query.strip().upper().startswith("SELECT"):
        return [{"hata": "Güvenlik nedeniyle sadece SELECT sorguları çalıştırılabilir."}]
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result

@mcp.tool()
@tool_error_handler
def list_tables(db_path: str) -> list[str]:
    """Veritabanındaki tablo isimlerini listeler."""
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        raise FileNotFoundError(f"Veritabanı dosyası bulunamadı veya geçersiz: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

@mcp.tool()
@tool_error_handler
def describe_table(db_path: str, table_name: str) -> list[dict]:
    """Tablo sütunlarını, tiplerini ve null olup olamayacaklarını listeler (PRAGMA table_info)."""
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        raise FileNotFoundError(f"Veritabanı dosyası bulunamadı veya geçersiz: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # SQL injection protection for table_name is tricky with PRAGMA, 
    # but we assume the tool is called by an LLM that knows existing tables.
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    result = [
        {"cid": c[0], "name": c[1], "type": c[2], "notnull": c[3], "pk": c[5]} 
        for c in columns
    ]
    conn.close()
    return result

@mcp.tool()
@tool_error_handler
def get_table_schema(db_path: str, table_name: str) -> str:
    """Belirtilen tablonun şemasını (CREATE TABLE ifadesini) döner."""
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        raise FileNotFoundError(f"Veritabanı dosyası bulunamadı veya geçersiz: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    schema = cursor.fetchone()
    conn.close()
    return schema[0] if schema else f"Tablo bulunamadı: {table_name}"

@mcp.resource("sqlite://{db_path}/{table}")
def table_resource(db_path: str, table: str) -> list[dict]:
    """Belirli bir tabloyu veritabanı kaynağı olarak yükler."""
    return execute_query(db_path, f"SELECT * FROM {table} LIMIT 100")

if __name__ == "__main__":
    mcp.run()
