# Modül 5: Kendi MCP İstemcimizi (Host) Yazmak

Şu ana kadar hep **Server (Sunucu)** yani alet çantası yazdık. Ajanın "Mide"sini ve "Ellerini" kodladık, ancak "Beyin" olarak sürekli Claude Desktop veya Cursor'a muhtaç kaldık.

Bu modül, MCP'nin tam bağımsızlığa kavuştuğu yerdir. Claude uygulamasına muhtaç olmadan, doğrudan **MCP İstemci SDK'sını** kullanarak kendi ajan beyninizi nasıl yazacağınızı öğreneceksiniz.

## İçerik
- **İstemci Bağlantısı:** Bir sunucunun `stdio` kanalına Python üzerinden programatik olarak bağlanmak.
- **Araç Keşfi:** Server'ın sunduğu araçları asenkron olarak sorgulamak (`session.list_tools()`).
- **Araç Tetikleme:** Bir aracı argümanlarıyla birlikte çağırıp sonucunu kodunuza geri döndürmek (`session.call_tool()`).

## Uygulama Kodu
Uygulama örneğine [src/05_mcp_client_example/simple_agent.py](../src/05_mcp_client_example/simple_agent.py) dosyasından ulaşabilirsiniz.

## Nasıl Test Ederim?
Ana dizinde iseniz, Makefile komutunu kullanabilirsiniz:
```bash
make run-client
```
Bu komut, Modül 1'deki `hello_mcp` sunucusunu bir alt süreç olarak gizlice başlatır, ona mesaj atar, cevabını alır ve ekrana basar. Kendi Agentic sisteminizi kurmanın temel taşı budur.
