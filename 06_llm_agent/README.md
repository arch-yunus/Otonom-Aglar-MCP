# Modül 6: Tam Otonom Ajan (ReAct Döngüsü) ve LLM Entegrasyonu

Agentic AI tasarımlarının kusursuzlaşması için, MCP araçlarının (tools) bizim tarafımızdan değil, **düşünen bir yapay zeka** (LLM) tarafından otonom olarak tetiklenmesi gerekir. Bu konsepte endüstride **ReAct (Reason and Act - Düşün ve Eyleme Geç)** adı verilir.

Bu Büyük Final modülünde, Claude API (Anthropic) uygulamasını kullanarak MCP İstemcimize (Client) zeka ekliyoruz.

## Akış Mimarisi

1. **Bağlantı Kurulumu:** Ajanımız, MCP sunucusuna bağlanıp `session.list_tools()` ile tüm araçları JSON Schema olarak çeker.
2. **LLM'e Bilgi Verilmesi:** Ajan, elindeki araç listesini Anthropic API'ye tanıtarak "Benim bu yeteneklerim var, benden bir şey istendiğinde bu yetenekleri bana tetiklettir!" der.
3. **Eylem Kararı (Reason):** Kullanıcı "Bunu Büyük Harfe Çevir" dediğinde, LLM düşünür ve doğrudan cevap vermek yerine API'ye şu sinyali gönderir: `stop_reason: tool_use` (Araç kullanmam lazım).
4. **Gerçek Eylem (Act):** Python kodumuz, LLM'in bu kararını yakalar ve MCP sunucusundaki aracı fiziksel olarak çalıştırır.
5. **Döngünün Kapanması:** Araçtan dönen yanıt (Execution Result) tekrar LLM'e yollanır ve LLM kendi mantığıyla sonucu yorumlayarak kullanıcıya nihai cevabı sunar.

## Kurulum ve Uygulama
Öğretici script'i ( `autonomous_brain.py` ) çalıştırmak için:
1. `.env` dosyanıza kendi Anthropic (`ANTHROPIC_API_KEY`) anahtarınızı ekleyin.
2. `make run-llm` kısayolunu kullanın veya `python src/06_llm_agent/autonomous_brain.py` komutuyla doğrudan tetikleyin.

Bu kod mantığını Modül 3'te yazdığımız "Web Scraper" sunucusuyla birleştirdiğiniz an, elinizde internette araştırma yapıp sonuç özetleyen, son teknoloji bir **Bilişsel Otonom Ajanınız** olur!
