import os
import sys
import json
import numpy as np
from typing import List, Dict, Any, Optional

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.utils import create_mcp_server, setup_logging, tool_error_handler

# Modül 4: İleri Seviye Sistemler - Semantik Hafıza (Vector Store) Sunucusu v2
# Bu sürüm gerçek 'embeddings' kullanarak anlamsal arama yapar.
setup_logging()
mcp = create_mcp_server("Semantik Hafıza Sunucusu")

MEMORY_FILE = os.getenv("MCP_SEMANTIC_MEMORY_FILE", "semantic_memory.json")

# LLM tabanlı anlamsal arama için 'SentenceTransformers' kütüphanesini kullanıyoruz.
try:
    from sentence_transformers import SentenceTransformer
    # Küçük ama etkili bir model kullanıyoruz (yaklaşık 80-100MB)
    model = SentenceTransformer('all-MiniLM-L6-v2')
except ImportError:
    model = None
    print("UYARI: sentence-transformers yüklü değil. Basit arama moduna geçiliyor.")

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

def cosine_similarity(v1, v2):
    """İki vektör arasındaki kosinüs benzerliğini hesaplar."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2) if norm_v1 > 0 and norm_v2 > 0 else 0

@mcp.tool()
@tool_error_handler
def store_knowledge(content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
    """Bilgiyi semantik hafızaya kaydeder. Otomatik olarak vektör (embedding) oluşturulur."""
    memory = load_memory()
    
    embedding = None
    if model:
        # Vektörü oluştur ve listeye çevir (JSON serileştirme için)
        embedding = model.encode(content).tolist()
    
    entry = {
        "content": content,
        "embedding": embedding,
        "metadata": metadata or {},
        "timestamp": os.path.getmtime(MEMORY_FILE) if os.path.exists(MEMORY_FILE) else 0
    }
    memory.append(entry)
    save_memory(memory)
    return "BİLGİ: Gerçek vektör verisiyle semantik hafızaya kaydedildi."

@mcp.tool()
@tool_error_handler
def search_knowledge(query: str, top_k: int = 3) -> List[str]:
    """
    Belirtilen 'query' ile anlamsal (vektörel) olarak en yakın bilgileri getirir.
    'I love cats' sorgusu 'Felines are great' sonucunu bulabilir.
    """
    memory = load_memory()
    if not memory:
        return ["Hafıza henüz boş."]
    
    if not model or not memory[0].get("embedding"):
        # Fallback: Basit kelime bazlı arama
        query_words = set(query.lower().split())
        scored_results = []
        for item in memory:
            content_words = set(item["content"].lower().split())
            score = len(query_words.intersection(content_words)) / len(query_words) if query_words else 0
            scored_results.append((score, item["content"]))
    else:
        # Gelişmiş Vektörel Arama
        query_embedding = model.encode(query)
        scored_results = []
        for item in memory:
            if item.get("embedding"):
                score = cosine_similarity(query_embedding, np.array(item["embedding"]))
                scored_results.append((score, item["content"]))
    
    scored_results.sort(key=lambda x: x[0], reverse=True)
    results = [text for score, text in scored_results[:top_k] if score > 0.3] # %30 benzerlik eşiği
    
    return results if results else ["Eşleşen anlamsal bilgi bulunamadı."]

if __name__ == "__main__":
    mcp.run()
