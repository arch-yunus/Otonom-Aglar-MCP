import asyncio
import os
import sys

# Ensure src is in Python path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Modül 5: Kendi MCP İstemcimizi (Host) Yazmak
# Bu betik, Claude Desktop olmadan własne (kendi) ajanlarınızı nasıl yazacağınızı gösterir.

async def run_client():
    """
    Basit bir İstemci (Client). 
    Modül 1'de yazdığımız hello_mcp.py sunucusuna bağlanır,
    aracını (tool) bulur ve onu tetikler.
    """
    print("Modül 5 Başlıyor: MCP Client'ı başlatılıyor...")
    
    # Hedef Sunucunun Yolu
    server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01_core_mechanics", "hello_mcp.py"))
    
    # Sunucuya Stdio (Standart İletişim) üzerinden bağlanmak için parametreler
    # Tıpkı Claude'un json config ile yaptığı şeyi biz Python ile yapıyoruz.
    server_params = StdioServerParameters(
        command="python",
        args=[server_path],
    )

    print(f"Sunucuya Bağlanılıyor: {server_path}")
    
    # İstemci ile sunucu arasında köprü kur (JSON-RPC)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. MCP El Sıkışma (Handshake) Adımı
            await session.initialize()
            print("\n✅ Sunucu ile bağlantı (Handshake) başarılı!")

            # 2. Sunucudaki Araçları Keşfet
            print("\n🔍 Sunucudaki Araçlar Keşfediliyor...")
            tools_response = await session.list_tools()
            
            tool_names = [tool.name for tool in tools_response.tools]
            print(f"Bulunan Araçlar: {', '.join(tool_names)}")
            
            if "to_upper" in tool_names:
                # 3. Aracı Tetikle
                print("\n🚀 'to_upper' Aracı LLM adına Otonom Olarak Tetikleniyor...")
                test_text = "mcp protokolü harika!"
                print(f"Gönderilen Metin: '{test_text}'")
                
                result = await session.call_tool("to_upper", arguments={"text": test_text})
                
                # Sonucu oku
                # FastMCP/MCP SDK >= 1.0.0 uses Content objects in result.content
                final_text = result.content[0].text
                print(f"\n🎉 Sunucunun Aracı Çalıştırdıktan Sonraki Yanıtı: '{final_text}'")
            else:
                print("Beklenen araç bulunamadı.")

if __name__ == "__main__":
    # Event loop'u çalıştır
    asyncio.run(run_client())
