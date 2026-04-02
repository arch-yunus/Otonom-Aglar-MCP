import os
import sys
import asyncio
from dotenv import load_dotenv

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# MCP imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# LLM imports
try:
    import anthropic
except ImportError:
    print("Lütfen önce bağımlılıkları yükleyin: pip install anthropic")
    sys.exit(1)

load_dotenv()

# Modül 6: Tam Otonom Ajan (ReAct Döngüsü)
# LLM'lerin sadece araçları görmesini değil, "Düşün-Eyleme Geç" 
# döngüsüyle bu araçları kendi inisiyatifiyle kullanmasını sağlar.

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

async def run_autonomous_agent():
    if not ANTHROPIC_API_KEY:
        print("HATA: ANTHROPIC_API_KEY bulunamadı. Lütfen .env dosyanızı güncelleyin.")
        return

    # Hedef MCP Sunucumuz
    server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01_core_mechanics", "hello_mcp.py"))
    server_params = StdioServerParameters(command="python", args=[server_path])

    print("🧠 Düşünen Ajan (Autonomous Brain) Başlatılıyor...\n")
    
    # Anthropic Claude API İstemcisi
    llm_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_session:
            await mcp_session.initialize()
            
            # Sunucudan araçları alıp Anthropic'in anladığı formata çeviriyoruz
            tools_response = await mcp_session.list_tools()
            
            anthropic_tools = []
            for tool in tools_response.tools:
                anthropic_tools.append({
                    "name": tool.name,
                    "description": tool.description or "",
                    "input_schema": tool.inputSchema
                })
                
            print(f"🔧 Sunucudan Entegre Edilen Araçlar: {[t['name'] for t in anthropic_tools]}\n")
            
            # --- ReAct Döngüsü Başlıyor ---
            user_prompt = "Merhaba Claude, elimizdeki to_upper aracını kullanarak 'Otonom yapay zeka harikadır' cümlesini büyük harfe çevir ve sonucu bana doğrudan göster."
            print(f"👤 KULLANICI: {user_prompt}\n")
            
            messages = [{"role": "user", "content": user_prompt}]
            
            # 1. Aşama: LLM'e araçların listesiyle soruyu sor
            print("⏳ Ajan Düşünüyor (LLM API Çağrısı)...")
            response = llm_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                tools=anthropic_tools,
                messages=messages
            )
            
            # 2. Aşama: LLM araç kullanmak istiyor mu?
            if response.stop_reason == "tool_use":
                tool_use = next(block for block in response.content if block.type == "tool_use")
                tool_name = tool_use.name
                tool_args = tool_use.input
                
                print(f"🤖 AJAN KARARI: '{tool_name}' aracını kullanmak istiyorum. Parametreler: {tool_args}")
                
                # 3. Aşama: Gerçek Eylem (Action) - MCP Üzerinden Python Fonksiyonunu Tetikle
                mcp_result = await mcp_session.call_tool(tool_name, arguments=tool_args)
                tool_result_text = mcp_result.content[0].text
                print(f"⚙️ SUNUCU CIŞTISI (Execution Result): {tool_result_text}")
                
                # 4. Aşama: Sonucu alıp LLM'e geri besle ve final yanıtını iste
                messages.append(
                    {"role": "assistant", "content": response.content}
                )
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use.id,
                                "content": tool_result_text,
                            }
                        ],
                    }
                )
                
                print("\n⏳ Ajan Çıktıyı Değerlendirip Final Cevabını Üretiyor...")
                final_response = llm_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    tools=anthropic_tools,
                    messages=messages
                )
                
                print(f"\n🧠 AJANIN FİNAL YANITI:\n{final_response.content[0].text}")
            else:
                print(f"\n🧠 AJANIN YANITI (Araç kullanmaya gerek kalmadı):\n{response.content[0].text}")

if __name__ == "__main__":
    asyncio.run(run_autonomous_agent())
