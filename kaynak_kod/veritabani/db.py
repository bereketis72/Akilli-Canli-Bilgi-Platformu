import pyodbc

server = r"Bereket\SQLEXPRESS02"
database = "bilgi_platform"
username = "sa"
password = "727272"

def kategori_belirle(baslik, metin):
    baslik_kucuk = baslik.lower().strip()
    metin_kucuk = (baslik+" " +metin).lower()

    
  
    bitki_isimleri = ["gül", "rose", "menekşe", "violet", "lale", "tulip", "papatya", "daisy", 
                      "orkide", "orchid", "sunflower", "ayçiçeği", "lotus", "lily", "zambak"]
    hayvan_isimleri = ["aslan", "lion", "kaplan", "tiger", "köpek", "dog", "kedi", "cat", 
                       "kartal", "eagle", "balina", "whale", "penguin", "penguen", "elephant", "fil"]
    
    for isim in bitki_isimleri:
        if isim in baslik_kucuk:
            return "Bitki"
    for isim in hayvan_isimleri:
        if isim in baslik_kucuk:
            return "Hayvan"
    

    hayvan_kelimeleri = [
        "animal", "mammal", "bird", "fish", "reptile", "insect", "species",
        "hayvan", "memeli", "kuş", "balık", "sürüngen", "böcek", "tür",
        "predator", "prey", "hunt", "carnivore", "herbivore",
        "yırtıcı", "av", "avlanır", "etobur", "otobur",
        "wildlife", "zoo", "habitat", "yavru", "offspring"
    ]
    
    bitki_kelimeleri = [
        "plant", "flower", "leaf", "seed", "tree", "root", "stem", "petal",
        "bitki", "çiçek", "yaprak", "tohum", "ağaç", "kök", "gövde", "taç yaprak",
        "botanical", "flora", "garden", "bloom", "pollen",
        "botanik", "flora", "bahçe", "açar", "polen",
        "flowering", "perennial", "annual", "shrub"
    ]
    
    hayvan_skor = sum(1 for kelime in hayvan_kelimeleri if kelime in metin_kucuk)
    bitki_skor = sum(1 for kelime in bitki_kelimeleri if kelime in metin_kucuk)
    
    
    if bitki_skor > hayvan_skor:
        return "Bitki"
    elif hayvan_skor > bitki_skor:
        return "Hayvan"
    else:
        return "Diger"
def baglanti_kur():
    try:
        conn_str = (
            f"driver={{SQL Server}};"
            f"server={server};"
            f"database={database};"
            f"uid={username};"
            f"pwd={password}"
        )
        return pyodbc.connect(conn_str)
    except Exception as e:
        print(f"veritabanı bağlantı hatası: {e}")
        return None
def canli_kaydet(c):
    baglanti = baglanti_kur()
    if not baglanti:
        return
    cursor = baglanti.cursor()
    temiz_baslik = str(c['baslik']).strip().capitalize()
    kategori = kategori_belirle(temiz_baslik, c['tam_metin'])
    sorgu = '''
        insert into canlinin_bilgileri
        (baslik, giris_ozeti, genel_ozet, tam_metin, url, kategori)
        values (?, ?, ?, ?, ?, ?)
    '''
    try:
        cursor.execute(sorgu, (
            temiz_baslik,
            c['giris_ozeti'],
            c.get('genel_ozet', ''),
            c['tam_metin'],
            c['url'],
            kategori
        ))
        baglanti.commit()
    except pyodbc.IntegrityError:
        print(f"ℹ{temiz_baslik} zaten mevcut.")
    except Exception as e:
        print(f"kayit hatasi: {e}")
    finally:
        baglanti.close()
def canli_getir(baslik):
    temiz_arama = str(baslik).strip()
    baglanti = baglanti_kur()
    if not baglanti:
        return None
    
    try:
        cursor = baglanti.cursor()
        sorgu = "select baslik, giris_ozeti, genel_ozet, tam_metin, url, kategori from canlinin_bilgileri where lower(baslik) = lower(?)"
        cursor.execute(sorgu, (temiz_arama,))
        row = cursor.fetchone()
        if row:
            return {
                "baslik": row[0],
                "giris_ozeti": row[1],
                "genel_ozet": row[2],
                "tam_metin": row[3],
                "url": row[4],
                "kategori": row[5]
            }
    except Exception as e:
        print(f" hata: {e}")
    finally:
        baglanti.close()
    return None
def kategoriye_gore_listele(kategori=None):
    baglanti = baglanti_kur()
    if not baglanti:
        return []
    
    try:
        cursor = baglanti.cursor()
        if kategori:
            cursor.execute("select baslik,url,kategori from canlinin_bilgileri where kategori = ?", (kategori,))
        else:
            cursor.execute("select baslik ,url,kategori from canlinin_bilgileri")
        rows = cursor.fetchall()
        return [{"baslik": r[0], "url": r[1], "kategori": r[2]} for r in rows]
    except Exception as e:
        print(f"listeleme hatası: {e}")
        return[]
    finally:
        baglanti.close()
if __name__ == "__main__":
    conn = baglanti_kur()
    if conn:
        print("Database bağlantısı başarılı!")
        conn.close()