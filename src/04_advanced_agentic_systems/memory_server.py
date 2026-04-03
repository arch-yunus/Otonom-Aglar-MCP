import json
import os
import sys

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.utils import create_mcp_server, setup_logging, tool_error_handler

# Modül 4: İleri Seviye Sistemler - Otonom Hafıza (State) Sunucusu
setup_logging()
mcp = create_mcp_server("Ajan Hafıza Sunucusu")

# Basit bir JSON kalıcılık dosyası
MEMORY_FILE = os.getenv("MCP_MEMORY_FILE", "agent_memory.json")

def _load_memory() -> dict:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_memory(data: dict):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@mcp.tool()
@tool_error_handler
def log_task_progress(task_id: str, status: str, details: str) -> str:
    """Otonom bir görevin ilerlemesini günlüğe yazar. Nerede kaldığınızı hatırlatır."""
    memory = _load_memory()
    if "tasks" not in memory:
        memory["tasks"] = {}
        
    memory["tasks"][task_id] = {
        "status": status,
        "details": details,
        "timestamp": os.path.getmtime(MEMORY_FILE) if os.path.exists(MEMORY_FILE) else None
    }
    _save_memory(memory)
    return f"GÖREV KAYDI: '{task_id}' durumu '{status}' olarak güncellendi."

@mcp.tool()
@tool_error_handler
def get_task_status(task_id: str) -> str:
    """Belirli bir görevin son durumunu hafızadan getirir."""
    memory = _load_memory()
    task = memory.get("tasks", {}).get(task_id)
    if task:
        return f"DURUM: {task['status']} | DETAY: {task['details']}"
    return f"HATA: '{task_id}' kimlikli görev bulunamadı."

@mcp.tool()
@tool_error_handler
def get_all_active_tasks() -> dict:
    """Hafızadaki tüm görevleri ve durumlarını toplu halde gösterir."""
    memory = _load_memory()
    return memory.get("tasks", {})

@mcp.tool()
@tool_error_handler
def clear_memory() -> str:
    """Tüm hafızayı sıfırlar (Tehlikeli işlem!)."""
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    return "BİLGİ: Ajan hafızası tamamen temizlendi."

if __name__ == "__main__":
    mcp.run()
