# Akıllı Canlı Bilgi Platformu

> Yapay zeka destekli, Wikipedia tabanlı otomatik canlı bilgi sistemi

---

---

## Ekran Görüntüleri

### Ana Sayfa
![Ana Sayfa](screenshots/anasayfa.png)

### Dijital Kimlik Kartı
![Dijital Kimlik Kartı](screenshots/dijital_kimlik.png)

### Detaylı Bilgi Görünümü
![Detaylı Görünüm](screenshots/detay_gorunum.png)

### Akıllı Öneri Sistemi
![Öneri Sistemi](screenshots/oneriler.png)

---

## Proje Hakkında

Bu proje, **Wikipedia verilerini** kullanarak hayvanlar ve bitkiler hakkında otomatik "**Dijital Kimlik Kartları**" oluşturan, yapay zeka destekli bir bilgi platformudur. Karmaşık ve dağınık olan biyolojik bilgileri analiz eder, özetler ve kullanıcıya yapılandırılmış bir formatta sunar.

### Temel Amaç

Geniş kapsamlı ancak dağınık olan biyolojik bilgileri süzerek kullanıcıya en kritik verileri sunmak:
- **Bilimsel Ad**
- **Familya Bilgisi**
- **Habitat/Yaşam Alanı**
- **Beslenme Şekli**
- **Tehdit Durumu**
- **İlginç Bilgiler**

Sistem, İngilizce gibi zengin kaynakları anlık olarak **otomatik Türkçeye çevirerek** dil bariyerini ortadan kaldırır ve kullanıcıya temiz, minimalist bir arayüz sağlar.

---

## Özellikler

### Yapay Zeka & NLP Özellikleri

- **Otomatik Dil Çevirisi**: İngilizce Wikipedia verilerini Google Translate API ile Türkçeye çevirir
- **Akıllı Kategorilendirme**: Metinlerdeki anahtar kelimeleri analiz ederek canlıyı "Bitki", "Hayvan" veya "Diğer" kategorilerine ayırır
- **Skor Tabanlı Sınıflandırma**: Kategori belirlenemediğinde, metindeki hayvan/bitki kelimelerini sayarak en yüksek skora göre sınıflandırır
- **Akıllı Özetleme**: Binlerce kelimelik Wikipedia makalelerini anlamsal olarak en güçlü 10-15 cümleye indirger
- **Regex Tabanlı Veri Çıkarma**: Bilimsel ad, familya, habitat gibi kritik bilgileri metinden otomatik olarak tespit eder

### Veritabanı & Performans

- **Akıllı Önbellekleme (Caching)**: Aynı canlı tekrar arandığında veritabanından saniyeler içinde getirilir
- **SQL Server Entegrasyonu**: Kalıcı veri saklama ve hızlı sorgulama
- **Otomatik Veri Kaydı**: Yeni aranan canlılar otomatik olarak veritabanına kaydedilir

### Kullanıcı Deneyimi

- **Dijital Kimlik Kartları**: Her canlı için detaylı, yapılandırılmış bilgi kartları
- **Akıllı Öneri Sistemi**: Kullanıcının aradığı canlıya göre rastgele keşif önerileri sunar
- **Web Arayüzü**: Modern, kullanıcı dostu HTML arayüzü
- **RESTful API**: Tüm özelliklere programatik erişim

---



### Dosya Yapısı ve Sorumluluklar

#### **`api/api.py`** - Genel Yönetici
```
 Rol: Orkestrasyondan sorumlu ana kontrol merkezi
```
- Tüm HTTP isteklerini yönetir
- Veritabanı ve Wikipedia modüllerini koordine eder
- Çeviri işlemlerini gerçekleştirir
- Web arayüzünü sunar

**Ana Endpoint'ler:**
- `GET /` - Web arayüzü
- `GET /ara?konu=...` - Canlı bilgisi sorgulama
- `GET /kimlik/{canli}` - Dijital kimlik kartı
- `GET /oneriler/{canli}` - Benzer canlı önerileri
- `GET /liste` - Tüm kayıtlı canlıları listele

---

#### **`veri_kaynaklari/wikipedia.py`** - Veri Madencisi
```
Rol: Dış dünyaya açılan veri toplama kapısı
```
- Wikipedia'dan ham veri çeker
- İngilizce içeriği otomatik Türkçeye çevirir
- 4000 karakterden uzun metinleri parçalara bölerek çevirir
- Anlam ayrımı sayfalarını tespit eder ve filtreler

**Özellikler:**
- Akıllı metin parçalama (4000 karakter limiti)
- Anlam ayrımı tespiti
- Hata yönetimi ve fallback mekanizmaları

---

#### **`dogal_dil_isleme/canli_kimligi.py`** - NLP Analiz Uzmanı
```
 Rol: Metinlerden kritik bilgileri çıkaran zeka motoru
```
- **Bilimsel Ad Tespiti**: Regex ile parantez içindeki Latince isimleri bulur
- **Familya Belirleme**: 14+ farklı familyanı (Felidae, Canidae, vb.) tespit eder
- **Habitat Analizi**: Kıtalar, kutup bölgeleri ve ortamları (orman, çöl, okyanus) belirler
- **Beslenme Şekli**: Etobur, otobur, hepçil, fotosentez yapan ayrımı yapar
- **Tehdit Durumu**: IUCN kategorilerine göre koruma durumunu belirler
- **İlginç Bilgi**: "En büyük", "en hızlı" gibi superlatifleri içeren cümleleri seçer

**Kullanılan Teknikler:**
- Regex pattern matching
- Keyword density analysis
- Multi-language keyword matching (EN/TR)

---

#### **`dogal_dil_isleme/ozetleyici.py`** - Akıllı Editör
```
Rol: Uzun metinleri anlamlı özetlere dönüştürme
```
- Wikipedia makalelerini analiz eder
- Anlamsal olarak en güçlü cümleleri seçer
- Bilgi yoğunluğu yüksek içeriği önceliklendirir
- 10-15 cümlelik akıcı özetler oluşturur

**Kullanılan Kütüphane:** `sumy` (Extraction-based summarization)

---

#### **`veritabani/db.py`** - Hafıza Merkezi
```
Rol: Kalıcı veri saklama ve hızlı erişim
```
- SQL Server bağlantı yönetimi
- CRUD operasyonları
- Otomatik kategori belirleme sistemi
- Duplicate kayıt kontrolü

**Kategori Belirleme Algoritması:**
1. **İlk Kontrol**: Başlıkta direkt isim var mı? (gül, aslan, vb.)
2. **İkinci Kontrol**: Metinde hayvan/bitki kelimeleri sayılır (skor sistemi)
3. **Karar**: En yüksek skora göre "Bitki" veya "Hayvan" kategorisi atanır

```python
hayvan_kelimeleri = ["mammal", "predator", "hunt", ...]
bitki_kelimeleri = ["plant", "flower", "seed", ...]

hayvan_skor = sum(1 for kelime in hayvan_kelimeleri if kelime in metin)
bitki_skor = sum(1 for kelime in bitki_kelimeleri if kelime in metin)
```

---

#### **`makine_ogrenmesi/benzerlik.py`** - Keşif Sistemi
```
Rol: Kullanıcı deneyimini artıran öneri motoru
```
- 50+ hazır canlı havuzu
- Rastgele ama alakalı öneri üretimi
- Kategori bazlı (Hayvan/Bitki) öneri filtreleme
- Her aramada farklı keşif deneyimi

**Öneri Havuzu Örnekleri:**
- **Hayvanlar**: Aslan, Kaplan, Fil, Penguen, Yunus, Köpekbalığı...
- **Bitkiler**: Gül, Orkide, Lale, Meşe, Bambu, Kaktüs...

---

## Teknoloji Yığını

### Backend Framework
| Teknoloji | Versiyon | Kullanım Amacı |
|-----------|----------|----------------|
| **FastAPI** | 0.100+ | Yüksek performanslı REST API framework'ü |
| **Uvicorn** | Latest | ASGI sunucu motoru |
| **Python** | 3.8+ | Ana programlama dili |

### Veri İşleme & AI
| Teknoloji | Kullanım Amacı |
|-----------|----------------|
| **Wikipedia-API** | Wikipedia verilerine programatik erişim |
| **Deep-Translator** | Google Translate tabanlı otomatik çeviri |
| **Sumy** | Extraction-based text summarization |
| **NLTK** | Natural Language Processing araçları |
| **Regex (re)** | Pattern matching ve veri çıkarma |

### Veritabanı
| Teknoloji | Kullanım Amacı |
|-----------|----------------|
| **SQL Server** | Kalıcı veri saklama |
| **PyODBC** | Python-SQL Server köprüsü |

### Veri Analizi
| Teknoloji | Kullanım Amacı |
|-----------|----------------|
| **Pandas** | Veri manipülasyonu |
| **Requests** | HTTP istekleri |

---

## Kurulum

### Ön Gereksinimler

- Python 3.8 veya üzeri
- SQL Server (LocalDB, Express veya Full sürüm)
- İnternet bağlantısı (Wikipedia ve çeviri API'leri için)

### Adım 1: Projeyi Klonlayın

```bash
git clone https://github.com/bereketis72/bilgi-platformu.git
cd bilgi-platformu
```

### Adım 2: Sanal Ortam Oluşturun (Önerilir)

#### Sanal Ortam (Virtual Environment) Nedir ve Neden Kullanırız?

**Sanal ortam**, Python projeleriniz için izole edilmiş bir çalışma alanıdır. Bunu neden kullanmalıyız?

**Problemler (Sanal Ortam Kullanmazsak):**
- Farklı projeler farklı kütüphane versiyonları gerektirebilir (Proje A: FastAPI 0.95, Proje B: FastAPI 0.110)
- Sistem genelinde yüklenen paketler birbirleriyle çakışabilir
- Proje bağımlılıklarını temiz tutmak zor olur
- Başka bir bilgisayara taşıma yaparken hangi paketlerin gerekli olduğunu bilmek zor

**Çözümler (Sanal Ortam Kullanırsak):**
- Her proje kendi bağımsız paket setine sahip olur
- Farklı projelerde farklı versiyon kullanabilirsiniz
- Sistem Python'unuz temiz kalır
- 'requirements.txt` ile bağımlılıklar net bir şekilde tanımlanır
- Proje kolayca başka bir ortama taşınabilir

#### Sanal Ortam Oluşturma ve Aktifleştirme

```bash
# 1. Sanal ortam klasörü oluştur (sadece ilk kez)
python -m venv venv

# 2. Sanal ortamı aktifleştir (her terminal açışında)

# Windows (PowerShell veya CMD)
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**Aktifleştirme başarılı olduğunda** terminal komut satırınızın başında `(venv)` yazısını göreceksiniz:


(venv) C:\Users\KULLANICI_ADI\bilgi_platformu>

> **İpucu:** Sanal ortamdan çıkmak için `deactivate` komutunu kullanabilirsiniz.

> **Önemli:** Her yeni terminal penceresi açtığınızda sanal ortamı tekrar aktifleştirmeniz gerekir!

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

**`requirements.txt` içeriği:**
```
wikipedia-api
fastapi
uvicorn
sumy
nltk
pandas
pyodbc
deep-translator
requests
```

### Adım 4: NLTK Verilerini İndirin

```bash
python -c "import nltk; nltk.download('punkt')"
```

### Adım 5: Veritabanını Hazırlayın

SQL Server'da aşağıdaki sorguları çalıştırın:

```sql
-- Veritabanı oluştur
CREATE DATABASE bilgi_platform;
GO

USE bilgi_platform;
GO

-- Tablo oluştur
CREATE TABLE canlinin_bilgileri (
    id INT PRIMARY KEY IDENTITY(1,1),
    baslik NVARCHAR(255) UNIQUE NOT NULL,
    giris_ozeti NVARCHAR(MAX),
    genel_ozet NVARCHAR(MAX),
    tam_metin NVARCHAR(MAX),
    url NVARCHAR(500),
    kategori NVARCHAR(50),
    kayit_tarihi DATETIME DEFAULT GETDATE()
);
GO
```

### Adım 6: Veritabanı Bağlantısını Yapılandırın

`kaynak_kod/veritabani/db.py` dosyasındaki bağlantı bilgilerini düzenleyin:

```python
server = r"SUNUCU_ADI\INSTANCE_ADI"  # Örnek: "localhost\SQLEXPRESS"
database = "bilgi_platform"
username = "KULLANICI_ADI"  # Örnek: "sa"
password = "ŞIFRE"
```

### Adım 7: Uygulamayı Başlatın

```bash
cd kaynak_kod
python api/api.py
```

Uygulama otomatik olarak **http://127.0.0.1:8001** adresinde tarayıcınızda açılacaktır! 🎉

---

## API Endpoints

### 1. Web Arayüzü
```http
GET /
```
**Açıklama:** Ana HTML arayüzünü gösterir

---

### 2. Canlı Bilgisi Sorgulama
```http
GET /ara?konu=aslan
```

**Parametreler:**
- `konu` (string, gerekli): Aranacak canlının adı (Türkçe veya İngilizce)

**Yanıt Örneği:**
```json
{
  "kaynak": "wikipedia",
  "baslik": "Aslan",
  "ozet": "Aslan (Panthera leo), kedigiller familyasından bir memeli türüdür. Afrika'nın savanlarında yaşar...",
  "url": "https://tr.wikipedia.org/wiki/Aslan"
}
```

**İşleyiş:**
1. Önce veritabanında kontrol edilir
2. Yoksa Türkçe → İngilizce çevrilir
3. Wikipedia'dan veri çekilir
4. İngilizce → Türkçe çevrilir
5. Özetlenir ve veritabanına kaydedilir

---

### 3. Dijital Kimlik Kartı
```http
GET /kimlik/aslan
```

**Parametreler:**
- `canli` (string, path parametresi): Canlının adı

**Yanıt Örneği:**
```json
{
  "baslik": "Aslan",
  "bilimsel_adi": "Panthera leo",
  "familya": "Kedigiller (Felidae)",
  "habitat": "Afrika, Savan",
  "beslenme": "Etobur",
  "tehdit_durumu": "Hassas",
  "ilginc_bilgi": "Aslanlar, en büyük kedigiller arasında yer alır ve günde 20 saate kadar uyuyabilirler."
}


### 4. Benzer Canlı Önerileri
```http
GET /oneriler/aslan?limit=5
```

**Parametreler:**
- `canli` (string, path parametresi): Canlının adı
- `limit` (int, opsiyonel, varsayılan=5): Öneri sayısı

**Yanıt Örneği:**
```json
{
  "canli": "aslan",
  "oneri_sayisi": 5,
  "oneriler": [
    {
      "baslik": "Kaplan",
      "kategori": "Hayvan",
      "url": "https://tr.wikipedia.org/wiki/Kaplan"
    },
    {
      "baslik": "Çita",
      "kategori": "Hayvan",
      "url": "https://tr.wikipedia.org/wiki/Çita"
    }
  ]
}
```

---

### 5. Kayıtlı Canlıları Listele
```http
GET /liste
```

**Yanıt Örneği:**
```json
{
  "toplam": 42,
  "canlilar": [
    {
      "baslik": "Aslan",
      "url": "https://tr.wikipedia.org/wiki/Aslan"
    },
    {
      "baslik": "Gül",
      "url": "https://tr.wikipedia.org/wiki/Gül"
    }
  ]
}
```

---





## Veritabanı Şeması

```sql
Table: canlinin_bilgileri
┌──────────────┬────────────────┬─────────────┬──────────────┐
│ Column       │ Type           │ Constraint  │ Description  │
├──────────────┼────────────────┼─────────────┼──────────────┤
│ id           │ INT            │ PRIMARY KEY │ Otomatik ID  │
│ baslik       │ NVARCHAR(255)  │ UNIQUE      │ Canlı adı    │
│ giris_ozeti  │ NVARCHAR(MAX)  │             │ İlk özet     │
│ genel_ozet   │ NVARCHAR(MAX)  │             │ AI özeti     │
│ tam_metin    │ NVARCHAR(MAX)  │             │ Tam içerik   │
│ url          │ NVARCHAR(500)  │             │ Wikipedia URL│
│ kategori     │ NVARCHAR(50)   │             │ Bitki/Hayvan │
│ kayit_tarihi │ DATETIME       │ DEFAULT NOW │ Kayıt zamanı │
└──────────────┴────────────────┴─────────────┴──────────────┘
```



## Web Arayüzü

Proje, kullanıcı dostu bir HTML arayüzü ile birlikte gelir. Tarayıcınızda **http://127.0.0.1:8001** adresine gittiğinizde:

- Arama kutusu
- Sonuç kartları
- Dijital kimlik kartları
- Öneri bölümü

görüntülenecektir.

---

## Gelecek Geliştirmeler

- [ ] **Görsel Analiz**: Canlı resimlerinden otomatik tür tanıma (Hugging Face)
- [ ] **Çoklu Dil Desteği**: İngilizce, Almanca, Fransızca arayüzler
- [ ] **Gelişmiş ML**: TF-IDF veya Word2Vec ile daha akıllı benzerlik önerileri
- [ ] **Kullanıcı Sistemi**: Favori canlılar, arama geçmişi
- [ ] **Export Fonksiyonu**: PDF/Excel olarak kimlik kartı indirme
- [ ] **API Rate Limiting**: Güvenlik ve performans iyileştirmeleri
- [ ] **Docker Support**: Kolay deployment

---


## 👤 Geliştirici

**Bereket İş**
- GitHub: [@bereketis72](https://github.com/bereketis72)
- LinkedIn: [linkedin.com/in/bereket-iş-161387314](https://linkedin.com/in/bereket-iş-161387314)
