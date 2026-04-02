import json
import os
from mcp.server.fastmcp import FastMCP

# Modül 4: İleri Seviye Sistemler - Otonom Hafıza (State) Sunucusu
# İşlemler asenkron veya uzun sürdüğünde LLM'in bağlamı hatırlamasını sağlar.

mcp = FastMCP("Ajan Hafıza Sunucusu")

# Basit bir JSON kalıcılık dosyası
MEMORY_FILE = "agent_memory.json"

def load_memory() -> dict:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(data: dict):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@mcp.tool()
def log_task_progress(task_id: str, status: str, details: str) -> str:
    """Otonom bir görevin ilerlemesini günlüğe yazar. Nerede kaldığınızı hatırlatır."""
    memory = load_memory()
    if "tasks" not in memory:
        memory["tasks"] = {}
        
    memory["tasks"][task_id] = {
        "status": status,
        "details": details
    }
    save_memory(memory)
    return f"Görev '{task_id}' başarıyla '{status}' olarak kaydedildi."

@mcp.tool()
def get_task_status(task_id: str) -> str:
    """Belirli bir görevin son durumunu hafızadan getirir."""
    memory = load_memory()
    task = memory.get("tasks", {}).get(task_id)
    if task:
        return f"Durum: {task['status']} - Detaylar: {task['details']}"
    return "Görev bulunamadı."

@mcp.tool()
def get_all_active_tasks() -> dict:
    """Hafızadaki tüm görevleri gösterir."""
    memory = load_memory()
    return memory.get("tasks", {})

if __name__ == "__main__":
    mcp.run()
