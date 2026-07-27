import os
import sys
import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import httpx

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# MCP imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from src.common.utils import setup_logging

# LLM imports
try:
    import anthropic
except ImportError:
    print("Lütfen önce bağımlılıkları yükleyin: pip install anthropic")
    sys.exit(1)

load_dotenv()
logger = setup_logging()

class AutonomousAgent:
    """
    Model Context Protocol (MCP) üzerinden dış dünya ile konuşan,
    Düşün-Eyleme Geç (ReAct) döngüsüyle otonom kararlar alan ajan sistemi.
    """
    
    def __init__(self, model: str = "claude-3-5-sonnet-20241022", log_callback: Optional[Any] = None):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY bulunamadı!")
            
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        self.history: List[Dict[str, Any]] = []
        self.mcp_sessions: List[ClientSession] = []
        self.available_tools: List[Dict[str, Any]] = []
        self.exit_stack = asyncio.ExitStack()
        self.log_callback = log_callback

    async def emit_log(self, log_type: str, message: str):
        """Log basar, varsa callback'e iletir ve HTTP ile Dashboard'a gönderir."""
        if log_type == "Success":
            logger.info(f"✅ {message}")
        elif log_type == "Error":
            logger.error(f"❌ {message}")
        elif log_type == "Warning":
            logger.warning(f"⚠️ {message}")
        else:
            logger.info(f"[{log_type}] {message}")

        if self.log_callback:
            try:
                self.log_callback(log_type, message)
            except Exception as e:
                logger.error(f"Callback hatası: {e}")

        # Dashboard'a HTTP POST olarak gönder (Arka planda çalışıyor olabilir)
        try:
            async with httpx.AsyncClient() as client:
                await client.post("http://localhost:5000/api/log", json={
                    "type": log_type,
                    "message": message
                }, timeout=1.0)
        except Exception:
            pass # Dashboard açık olmayabilir, sessizce geç

    async def connect_to_server(self, server_script: str):
        """Belirtilen MCP sunucusuna bağlanır ve araçlarını envantere ekler."""
        params = StdioServerParameters(command="python", args=[server_script])
        
        # Async context manager'ları dinamik yönetmek için contextlib kullanıyoruz
        transport = await self.exit_stack.enter_async_context(stdio_client(params))
        read, write = transport
        session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        
        await session.initialize()
        self.mcp_sessions.append(session)
        
        # Araçları listele ve Anthropic formatına çevir
        tools_response = await session.list_tools()
        for tool in tools_response.tools:
            self.available_tools.append({
                "name": tool.name,
                "description": tool.description or "",
                "input_schema": tool.inputSchema
            })
        
        await self.emit_log("Info", f"Sunucu Bağlandı: {os.path.basename(server_script)} | Kayıtlı Araç: {len(tools_response.tools)}")

    async def _call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """İlgili MCP oturumunu bulup aracı çalıştırır."""
        for session in self.mcp_sessions:
            # Not: Burada araç isminin benzersiz olduğunu varsayıyoruz (Namespace çakışması kontrolü eklenebilir)
            try:
                result = await session.call_tool(name, arguments=arguments)
                if result and result.content:
                    return result.content[0].text
            except Exception:
                continue
        return f"HATA: '{name}' aracı hiçbir bağlı sunucuda bulunamadı veya çalışma hatası oluştu."

    async def run(self, task: str, max_steps: int = 10):
        """Ajanın otonom döngüsünü (ReAct) başlatır."""
        await self.emit_log("Info", f"GÖREV BAŞLATILDI: {task}")
        self.history = [{"role": "user", "content": task}]
        
        step = 0
        while step < max_steps:
            step += 1
            await self.emit_log("Info", f"Adım {step} / {max_steps} işleniyor...")
            
            # 1. Düşünme Aşaması (LLM'e sor)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                tools=self.available_tools,
                messages=self.history
            )
            
            # Yanıtı geçmişe ekle
            self.history.append({"role": "assistant", "content": response.content})
            
            # 2. Eylem Belirleme
            if response.stop_reason == "tool_use":
                tool_use = next(block for block in response.content if block.type == "tool_use")
                thought = next((b.text for b in response.content if b.type == 'text'), 'Araç kullanıyorum...')
                await self.emit_log("Thought", thought)
                await self.emit_log("Action", f"Araç Çağrısı: {tool_use.name}({json.dumps(tool_use.input)})")
                
                # Aracı çalıştır
                observation = await self._call_tool(tool_use.name, tool_use.input)
                await self.emit_log("Observation", observation)
                
                # Gözlemi LLM'e geri besle
                self.history.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": observation,
                        }
                    ],
                })
            else:
                # Döngü bitti (Final yanıt)
                final_text = response.content[0].text
                await self.emit_log("Success", f"Ajanın Final Cevabı:\n{final_text}")
                return final_text
                
        await self.emit_log("Warning", "Maksimum adım sayısına ulaşıldı.")
        return "Görev tamamlanamadı (Max Steps)."

    async def shutdown(self):
        """Bağlantıları güvenle kapatır."""
        await self.exit_stack.aclose()
        await self.emit_log("Info", "Tüm MCP bağlantıları kapatıldı.")

async def run_agent_workflow(task: str, model: str = "claude-3-5-sonnet-20241022", log_callback: Optional[Any] = None):
    """Ajanın sunucularını bağlar, görevi çalıştırır ve temizlik yapar."""
    agent = AutonomousAgent(model=model, log_callback=log_callback)
    base_src = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    servers = [
        os.path.join(base_src, "01_core_mechanics", "hello_mcp.py"),
        os.path.join(base_src, "02_local_servers", "file_system_server.py"),
        os.path.join(base_src, "02_local_servers", "sqlite_server.py"),
        os.path.join(base_src, "03_web_integrations", "web_scraper.py"),
        os.path.join(base_src, "04_advanced_agentic_systems", "memory_server.py")
    ]
    
    try:
        for s in servers:
            if os.path.exists(s):
                await agent.connect_to_server(s)
        
        result = await agent.run(task)
        return result
    except Exception as e:
        await agent.emit_log("Error", f"Ajan yürütme hatası: {str(e)}")
        return f"HATA: {str(e)}"
    finally:
        await agent.shutdown()

async def main():
    # Test Senaryosu: Terminal üzerinden çalıştırma
    demo_task = (
        "1. 'mcp_test' adında bir veritabanı oluştur (veya SQLite araçlarını kullan).\n"
        "2. Yerel dizindeki README.md dosyasını oku.\n"
        "3. Dosyadaki vizyon bölümünü büyük harfe çevir.\n"
        "4. Ajan hafızasına 'README analizi yapıldı' notunu ekle.\n"
        "Hepsini otonom olarak yap ve sonucu raporla."
    )
    await run_agent_workflow(demo_task)

if __name__ == "__main__":
    asyncio.run(main())
