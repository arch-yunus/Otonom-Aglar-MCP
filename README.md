# 🌐 Otonom-Ağlar-MCP (Model Context Protocol)

<div align="center">
  <img src="assets/mcp_repo_banner.png" alt="Otonom-Ağlar-MCP Banner" style="width: 100%; border-radius: 10px;" />
</div>
<br>

[![MCP Protocol](https://img.shields.io/badge/MCP-Standard_v1.0-blue?style=for-the-badge&logo=anthropic)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.11+-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Status](https://img.shields.io/badge/Status-Aktif_Geliştirme-success?style=for-the-badge)](#)
[![Meta-Engineering](https://img.shields.io/badge/Lab-Meta--Engineering_Research-8A2BE2?style=for-the-badge)](#)

> Büyük Dil Modellerini (LLM) dış dünyadan izole edilmiş birer "metin kutusu" olmaktan çıkarıp, otonom bir şekilde veri toplayan, karar alan ve sistemleri yöneten **akıllı ajanlara (Agentic AI)** dönüştürmek için hazırlanmış uçtan uca mimari rehberi ve geliştirme atölyesi.

---

## 🚀 Vizyon ve Felsefe: Neden MCP?

Yapay zeka mühendisliği, basit komutlar (prompt) yazılan dönemi geride bıraktı. Artık odak noktamız, sistemlerin birbirleriyle konuşabildiği **Otonom Sistemler ve Ajan Mühendisliği (Agentic Engineering)**. Ancak modelleri dış dünyaya bağlarken bugüne kadar standart bir yol yoktu; her API için ayrı bir entegrasyon, her platform için ayrı bir SDK gerekiyordu.

Anthropic tarafından açık kaynak olarak sunulan **Model Context Protocol (MCP)**, tıpkı cihazları bilgisayara bağlayan USB-C standardı gibi, yapay zeka asistanlarını veri kaynaklarına (yerel dosyalar, veritabanları, API'ler, kurumsal uygulamalar) tek ve evrensel bir dille bağlamanızı sağlar. 

**Otonom-Ağlar-MCP**, bu protokolü sadece teorik olarak değil, pratik ve otonom sistemler inşa ederek öğrenmek isteyenler için tasarlanmıştır. Bu repoda kodlanan her bir sunucu, modelin dış dünyadaki "elleri ve gözleri" olacaktır.

---

## 🏗️ Mimari Topoloji: MCP Nasıl Çalışır?

MCP, istemci-sunucu (client-server) modeline dayalı bir mimari kullanır. Sistem tasarımı şu katmanlardan oluşur:

1. **MCP Host (Ev Sahibi):** Claude Desktop, Cursor veya kendi geliştirdiğimiz arayüzler. LLM'in çalıştığı, kullanıcının komut girdiği ana merkezdir.
2. **MCP Client (İstemci):** Host uygulamasının içinde çalışan ve sunucularla protokol üzerinden çift yönlü iletişimi (JSON-RPC) yöneten aracı katman.
3. **MCP Server (Sunucu):** Bu reponun asıl odak noktası. Modellerin internete, veritabanlarına veya yerel dosya sistemlerine erişmesi için yazılan özel arka plan servisleridir.

### 🧩 MCP'nin Temel Yapı Taşları (Primitives)

MCP mimarisinde modelleri otonomlaştıran üç temel yapı taşı bulunur ve bu repoda her biri derinlemesine işlenmektedir:

* **Resources (Kaynaklar):** Modele sadece "okuma" yetkisi verilen verilerdir. (Örn: Modelin referans alması için bağlanan bir log dosyası veya API'den çekilen statik bir JSON verisi). `file://`, `postgres://` gibi URI şemalarıyla çalışır.
* **Tools (Araçlar):** Modelin dış dünyada "aksiyon" almasını sağlayan fonksiyonlardır. Model bu araçları kendi inisiyatifiyle çağırabilir. (Örn: İnternette arama yapma, bir veritabanına yeni kayıt ekleme, GitHub'da issue açma).
* **Prompts (İstem Şablonları):** Kullanıcıların veya modellerin belirli görevler için önceden tanımlanmış, parametrik istemlere ulaşmasını sağlayan yapıdır.

---

## 🗺️ Geliştirme Yol Haritası ve Modüller

Bu eğitim atölyesi, adım adım artan bir karmaşıklık hiyerarşisine göre tasarlanmıştır. Klasör yapısı modüllere ayrılmıştır:

### 📗 Modül 1: Temeller ve Protokol Mekaniği (`/01_core_mechanics`)
* **Protokolün Anatomisi:** JSON-RPC mesajlaşma yapısı, yaşam döngüsü (Lifecycle), `initialize` ve `ping` metodları.
* **İletişim Kanalları:** Standart Girdi/Çıktı (`stdio`) ile Server-Sent Events (`SSE`) arasındaki farklar ve kullanım senaryoları.
* **Ortam Kurulumu:** Python sanal ortamlarının hazırlanması, MCP SDK'sının sisteme entegrasyonu ve resmi Inspector aracı ile hata ayıklama (debugging).

### 📘 Modül 2: İlk Otonom Adım - Yerel Etkileşim (`/02_local_servers`)
* **Dosya Okuyucu Sunucusu:** Python tabanlı, modelin bilgisayardaki belirli klasörleri güvenle okumasını sağlayan mimari.
* **SQLite Entegrasyonu:** LLM'in yerel bir veritabanındaki tabloları okuması, SQL sorguları üretip bunları MCP üzerinden güvenli şekilde çalıştırması.
* *Uygulama:* Verilen bir Python projesinin klasör dizinini okuyup, kodları analiz ederek otomatik `README.md` üreten veya potansiyel hataları listeleyen yerel otonom asistan.

### 📙 Modül 3: Dış Dünya Entegrasyonları ve API'ler (`/03_web_integrations`)
* **Otonom Web Scraper:** İnternetteki sitelere istek atıp, HTML'i Markdown formatına çevirerek modele saf bilgi aktaran aracın inşası.
* **REST/SOAP API Sarmalayıcıları:** Harici servislerin (Örn: Hava durumu, kripto borsa verileri) verilerini modele gerçek zamanlı sunma.
* **GitHub API Bağlantısı:** Modelin sizin adınıza kod okuması, repoları analiz etmesi ve yeni commit analizleri yapabilmesi.
* *Uygulama:* Borsa verilerini çeken bir API ile haberleri okuyan bir scraper sunucusunu birleştirip, finansal analiz yapan otonom bir asistan oluşturma.

### 📕 Modül 4: İleri Seviye Sistemler ve Siber Güvenlik (`/04_advanced_agentic_systems`)
* **Güvenlik ve İzolasyon:** Modelin sistem komutlarına sınırsız erişimini engelleme (Sandboxing), Path Traversal (dizin atlama) saldırılarına karşı önlemler.
* **Çoklu Sunucu Orkestrasyonu:** Claude Desktop yapılandırma dosyasında (`claude_desktop_config.json`) aynı anda 3-4 farklı MCP sunucusunu çalıştırarak ajanın yetenek ağını genişletme.
* **Durum (State) Yönetimi:** Otonom işlemler uzun sürdüğünde işlemlerin asenkron yönetimi ve loglanması.

---

## 🔐 Güvenlik Paradigması

Otonom ajanlar tasarlarken en kritik nokta güvenliktir. Bu repodaki projelerde şu prensipler uygulanır:
1. **Prensipte En Az Ayrıcalık (Least Privilege):** Sunucular sadece belirtilen dizinlere veya spesifik API uç noktalarına erişebilir. Tüm sistem root yetkisiyle açılmaz.
2. **Kullanıcı Onayı (Human-in-the-Loop):** Yıkıcı olabilecek "Tool" kullanımlarında (dosya silme, veritabanına yazma, ödeme yapma) model işlemi başlatır ancak nihai onay MCP Host arayüzü üzerinden kullanıcıya bırakılır.
3. **Çevre Değişkenleri (Environment Variables):** Hassas API anahtarları asla koda gömülmez, `.env` dosyaları ve güvenli enjeksiyon yöntemleri kullanılır.

---

## 🛠️ Kurulum ve Çalıştırma Rehberi

Projeyi yerel makinenizde (özellikle Linux/Ubuntu veya WSL tabanlı sistemlerde) test etmek için aşağıdaki adımları izleyin:

### Ön Koşullar
- Python 3.11 veya üzeri.
- Git versiyon kontrol sistemi.
- (İsteğe bağlı) Claude Desktop uygulaması veya Cursor IDE (MCP destekleyen hostlar).

### Başlangıç

```bash
# 1. Repoyu makinenize klonlayın
git clone https://github.com/bahattinyunus/Otonom-Aglar-MCP.git

# 2. Çalışma dizinine geçin
cd Otonom-Aglar-MCP

# 3. Sanal ortam (Virtual Environment) oluşturun ve aktif edin
python -m venv venv

# Linux/macOS için:
source venv/bin/activate  
# Windows için:
# venv\Scripts\activate

# 4. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 5. Çevre değişkenlerini yapılandırın
cp .env.example .env
# .env dosyasını kendi API anahtarlarınız ile güncelleyin.
```

### Örnek Bir Sunucuyu Test Etme
MCP Inspector kullanarak yazılan sunucuyu tarayıcı üzerinden anında test edebilirsiniz:

```bash
# Modül 2'deki dosya okuyucu sunucusunu çalıştırıp test etmek için:
npx @modelcontextprotocol/inspector python src/02_local_servers/file_reader/server.py
```

---

## 📚 Kaynakça ve İleri Okuma
* [Model Context Protocol Resmi Dokümantasyonu](https://modelcontextprotocol.io)
* [Anthropic MCP GitHub Organizasyonu](https://github.com/modelcontextprotocol)
* Agentic Design Patterns (ReAct, Plan-and-Solve)

---

## 🤝 Katkıda Bulunma (Contributing)

Bu repo sürekli gelişen, açık kaynaklı bir mühendislik laboratuvarı olarak tasarlanmıştır. Eğer yeni bir veri tabanı için MCP wrapper yazdıysanız, farklı bir API entegrasyonu geliştirdiyseniz veya güvenlik iyileştirmesi bulduysanız Pull Request (PR) göndermekten çekinmeyin!

Lütfen katkıda bulunmadan önce projenin kök dizininde bulunan `CONTRIBUTING.md` ve `CODE_OF_CONDUCT.md` dosyalarını okuyun.

---

## 📜 Lisans

Bu proje, açık bilgi felsefesini desteklemek amacıyla **MIT Lisansı** altında lisanslanmıştır. Repodaki kodları kendi ticari projelerinizde de özgürce kullanabilirsiniz. Detaylar için `LICENSE` dosyasına bakabilirsiniz.

---

<div align="center">
  <b>Meta-Engineering Research Lab</b> bünyesinde, dijital dünyada otonomiyi inşa etmek gayesiyle <i>Dijital Seyyah</i> tarafından tasarlanmıştır. <br>
  (2026)
</div>