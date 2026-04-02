# 🎓 Agentic AI ve MCP Eğitim Rehberi

Yapay zeka dünyasında "üretken AI" (Generative AI) döneminden "eylemsel AI" (Agentic AI) dönemine geçiş yapıyoruz. Bu rehber, **Otonom-Ağlar-MCP** reposunu kullanarak bu felsefeyi nasıl kendi sistemlerinize entegre edeceğinizi adım adım öğretecektir.

---

## 1. Chatbot'lardan Otonom Ajanlara Evrim

Eskiden LLM'ler (Büyük Dil Modelleri) sadece birer **metin kutusuydu**. Onlara soru sorardınız, onlar da dünyadaki verilerini (eğitildikleri zamana kadar olan kısıtlı veriyi) kullanarak bir yanıt üretirdi. Eğer internetteki canlı bir veriyi, kişisel bilgisayarınızdaki bir dosyayı veya şirketinizin veritabanındaki özel bir tabloyu sorarsanız, size "Benim bu bilgiye erişimim yok" derlerdi.

**Agentic AI (Otonom Ajan)** ise bu modellere "eller" ve "gözler" verme sanatıdır. 
- Ajan sadece cevap veren bir bot değildir; **karar alır, alet (tool) kullanır ve çevresini manipüle eder.**
- Sizin verdiğiniz bir görevi (örn: "Son bir haftadaki hataları bul ve bana raporla") gerçekleştirmek için sırasıyla veritabanına bağlanmayı akıl eder, sorgu atar, gelen verideki sorunu analiz etmek için Github kodlarını okur ve finalde bir sunum hazırlar. 

İşte bu "aletleri (tools)" modele bağlamanın en modern, standart ve güvenli yolu **Model Context Protocol (MCP)**'dür.

---

## 2. MCP'nin Anatomisi: Nasıl Çalışır?

MCP'yi, bir USB-C kablosu olarak düşünebilirsiniz. Bilgisayarınıza dilediğiniz donanımı aynı kabloyla bağlayabilirsiniz. MCP de yapay zekayı dilediğiniz veritabanına, API'ye veya klasöre standart bir "dil" (JSON-RPC) üzerinden bağlar.

MCP Mimarisi 3 temel parçadan oluşur:

1. **MCP Host (Ev Sahibi / Beyin):** Claude Desktop App, Cursor IDE veya kendi yazacağınız bir arayüz. LLM'in çalıştığı, kullanıcının komut girdiği ana üst merkezdir.
2. **MCP Client (İstemci):** Beynin (Host) sistemle konuşmasını sağlayan elçidir.
3. **MCP Server (Sunucu / Alet Çantası):** Bizim bu repoda yazdığımız Python dosyalarıdır! Dış dünya ile etkileşime giren, verileri LLM'in anlayacağı şekle çeviren küçük, becerikli servislerdir.

> **💡 Kritik Bilgi:** LLM'e doğrudan "Şu SQL sorgusunu çalıştır" demiyoruz. Biz bir "SQLite MCP Server" yazıyoruz. Claude (Host), bu Server'a soruyor: "Elinde hangi araçlar var?". Server cevap veriyor: "Bende veri tabanını listeleme, şema okuma ve okuma sorgusu atma araçları var". Claude artık bunları ne zaman kendi takdiriyle kullanması gerektiğini biliyor!

---

## 3. Tool (Araç) Tasarlama Psikolojisi

Bir MCP Server'ına `@mcp.tool()` ile özellik eklerken en önemli kurallar şunlardır:

1. **İsimlendirme:** LLM araçların isimlerine bakarak karar verir. `fetch_data()` kötü bir isimdir. `get_linux_system_logs()` çok daha iyidir.
2. **Docstring (Açıklama):** Python fonksiyonunuzun altına yazdığınız açıklama (`"""..."""`) aslında **LLM'e okutulan gizli bir prompt'dur!**. "Bu aracı ne zaman kullanmalısın, parametreler ne işe yarar" bilgisini açıkça yazmalısınız.
3. **Küçük ve Özelleşmiş Araçlar:** Bir fonksiyonda çok fazla şey yapmayın. Unix felsefesini izleyin: Bir araç (tool) tek bir şeyi iyi yapsın.

---

## 4. Güvenlik ve "Sandboxing" (Modül 4 Pratiği)

Eğer LLM'e bir bilgisayarın komut satırını, silme veya değiştirme yetkisiyle açarsanız; LLM (halüsinasyon görerek veya kötü niyetli promptlara maruz kalarak) tüm sisteminizi bozabilir.

- **Least Privilege (En Az Ayrıcalık):** Sunucunuza asla `root` veya `sudo` yetkisi vermeyin.
- **Path Traversal (Dizin Atlama) Koruması:** Bir dosya okuyucu server yapıyorsanız, mutlaka modeli belirli bir klasöre hapsedin (Sandbox). `../../etc/passwd` gibi sistem dosyalarına erişmesini kod içinde manuel olarak engelleyin (**Bkz: Modül 4: secure_executor.py**).
- **Human In The Loop:** Yıkıcı olabilecek "Tool" kullanımlarında (silme, commit atma) mutlaka son onay insana (size) bırakılmalıdır.

---

## 5. Sıradaki Adımlar ve Pratik

Bu repoyu klonladıktan sonra yapmanızı önerdiğimiz çalışma rotası:

1. Modül 1'deki `hello_mcp.py`'ı inceleyin, araçların nasıl tanımlandığını görün.
2. Kendi bilgisayarınızda bir klasör oluşturun ve Modül 2'deki `file_system_server.py`'ı kullanarak Claude'a o klasördeki karmaşık bir Python kod setini okutturun ve "Bu koddaki mimari hatalar nelerdir?" diye sorun. Hızına şaşıracaksınız.
3. Modül 4'teki `claude_desktop_config.example.json` örneğindeki gibi **aynı anda birden fazla Server'ı** Claude'a bağlayıp, ajanın kendi kendine bir siteden veri çekip, sonra gelip sizin veritabanınıza (SQLite) yazdığını kendi gözlerinizle görün.

*İşte tam da bu anda, yapay zekanın sadece metin yazmadığına, dünyayı değiştirebildiğine ikna olacaksınız.*
