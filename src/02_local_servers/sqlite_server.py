import sqlite3
from mcp.server.fastmcp import FastMCP

# Modül 2: Yerel Sunucular - SQLite Veritabanı Sunucusu
# Bu sunucu yerel veritabanlarına LLM'in SQL üzerinden erişimini sağlar.

mcp = FastMCP("SQLite Veritabanı Sunucusu")

@mcp.tool()
def execute_query(db_path: str, query: str) -> list[dict]:
    """Belirtilen veritabanında salt okunur SQL sorgusu çalıştırır."""
    if not query.strip().upper().startswith("SELECT"):
        return [{"hata": "Güvenlik nedeniyle sadece SELECT sorguları çalıştırılabilir."}]
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        conn.close()
        return result
    except Exception as e:
        return [{"hata": f"Sorgu hatası: {str(e)}"}]

@mcp.tool()
def list_tables(db_path: str) -> list[str]:
    """Veritabanındaki tablo isimlerini listeler."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        return [f"Hata: {str(e)}"]

@mcp.tool()
def get_table_schema(db_path: str, table_name: str) -> str:
    """Belirtilen tablonun şemasını (DDL) döner."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        schema = cursor.fetchone()
        conn.close()
        return schema[0] if schema else f"Tablo bulunamadı: {table_name}"
    except Exception as e:
        return f"Hata: {str(e)}"

@mcp.resource("sqlite://{db_path}/{table}")
def table_resource(db_path: str, table: str) -> list[dict]:
    """Belirli bir tabloyu veritabanı kaynağı olarak yükler."""
    return execute_query(db_path, f"SELECT * FROM {table} LIMIT 100")

if __name__ == "__main__":
    mcp.run()
