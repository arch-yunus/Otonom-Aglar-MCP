import os
import sys
import json
import numpy as np
from typing import List, Dict, Any, Optional

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.utils import create_mcp_server, setup_logging, tool_error_handler

# Modül 4: İleri Seviye Sistemler - Semantik Hafıza (Vector Store) Sunucusu
# Bu sunucu LLM'in geçmiş deneyimlerini anlam (anlamsal) olarak aramasını sağlar.
setup_logging()
mcp = create_mcp_server("Semantik Hafıza Sunucusu")

MEMORY_FILE = os.getenv("MCP_SEMANTIC_MEMORY_FILE", "semantic_memory.json")

# Basit bir "Keyword/Embedding" simülasyonu (Demo için SentenceTransformers önerilir)
# Burada basit bir TF-IDF benzeri anlamsal eşleşme veya Mock Embedding kullanacağız.

def load_memory() -> List[Dict[str, Any]]:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_memory(data: List[Dict[str, Any]]):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@mcp.tool()
@tool_error_handler
def store_knowledge(content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
    """Bilgiyi semantik hafızaya kaydeder. Gelecekte benzer konular sorulduğunda hatırlanacaktır."""
    memory = load_memory()
    entry = {
        "content": content,
        "metadata": metadata or {},
        "timestamp": os.path.getmtime(MEMORY_FILE) if os.path.exists(MEMORY_FILE) else 0
    }
    memory.append(entry)
    save_memory(memory)
    return "BİLGİ: Semantik hafızaya başarıyla kaydedildi. 'search_knowledge' ile erişilebilir."

@mcp.tool()
@tool_error_handler
def search_knowledge(query: str, top_k: int = 3) -> List[str]:
    """
    Belirtilen 'query' ile semantik (anlamsal) olarak en yakın bilgileri getirir.
    LLM'in geçmişte öğrendiği veya yaptığı işlemleri hatırlaması için kullanılır.
    """
    memory = load_memory()
    if not memory:
        return ["Hafıza henüz boş."]
    
    # Basit kelime bazlı benzerlik skoru (Embedding kütüphanesi yoksa fallback)
    query_words = set(query.lower().split())
    scored_results = []
    
    for item in memory:
        content_words = set(item["content"].lower().split())
        overlap = len(query_words.intersection(content_words))
        score = overlap / len(query_words) if query_words else 0
        scored_results.append((score, item["content"]))
    
    # Skora göre sırala ve top_k dön
    scored_results.sort(key=lambda x: x[0], reverse=True)
    results = [text for score, text in scored_results[:top_k] if score > 0]
    
    return results if results else ["Eşleşen anlamsal bilgi bulunamadı."]

if __name__ == "__main__":
    mcp.run()
