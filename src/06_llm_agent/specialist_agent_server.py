import os
import sys
import asyncio
from typing import Dict, Any, List
from dotenv import load_dotenv

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.common.utils import create_mcp_server, setup_logging, tool_error_handler

# Modül 7: Recursive Multi-Agent Delegation - Uzman Ajan Sunucusu
# Bu sunucu, ana ajanın (Master Brain) daha küçük ve odaklanmış alt ajanlara 
# iş devretmesini (delegation) sağlar. MCP Protokolü üzerinde "Agent-to-Agent" mimarisi.

try:
    import anthropic
except ImportError:
    print("anthropic SDK gereklidir.")
    sys.exit(1)

load_dotenv()
setup_logging()
mcp = create_mcp_server("Uzman Kod Analisti (Sub-Agent)")

@mcp.tool()
@tool_error_handler
def analyze_and_fix_code(code: str, language: str = "python") -> str:
    """
    Karmaşık kod bloklarını derinlemesine analiz eder ve olası hataları 
    düzeltilmiş versiyonlarıyla raporlar. (Bu araç bir LLM tarafından yönetilir!)
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = (
        f"Sen uzman bir '{language}' yazılımcısısın. Aşağıdaki kodu analiz et, "
        "hataları bul ve sadece en iyi düzeltilmiş halini (açıklama yapmadan) 'Markdown' formatında dön:\n\n"
        f"```{language}\n{code}\n```"
    )
    
    # Alt ajan (Uzman) kendi LLM çağrısını yapar
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

@mcp.tool()
@tool_error_handler
def generate_unit_tests(code: str, framework: str = "pytest") -> str:
    """Belirtilen kod bloğu için kapsamlı birim testler (unit tests) üretir."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = (
        f"Aşağıdaki kod için {framework} kullanarak profesyonel birim testler yaz.\n\n"
        f"KOD:\n{code}"
    )
    
    response = client.messages.create(
        model="claude-3-5-haiku-20241022", # Daha hızlı haiku modelini kullanabiliriz
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

if __name__ == "__main__":
    mcp.run()
