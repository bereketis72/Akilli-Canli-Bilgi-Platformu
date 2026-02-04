import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from dogal_dil_isleme.canli_kimligi import dijital_kimlik_olustur
from fastapi import FastAPI, Query 
from fastapi.responses import HTMLResponse 
from veri_kaynaklari.wikipedia import veri_cek
from dogal_dil_isleme.ozetleyici import metni_ozetle
from veritabani.db import canli_getir, canli_kaydet, baglanti_kur
from deep_translator import GoogleTranslator
from makine_ogrenmesi.benzerlik import benzerlik

def turkce_ingilizce_cevir(kelime):
    try:
        sonuc = GoogleTranslator(source='tr', target='en').translate(kelime)
        return sonuc
    except:
        return kelime

def ingilizce_turkce_cevir(kelime):
    try:
        sonuc = GoogleTranslator(source='en', target='tr').translate(kelime)
        return sonuc
    except:
        return kelime


app = FastAPI(
    title='Bilgi Platform API',
    version="1.0.0"
)

benzerlik_ = benzerlik()
@app.get("/oneriler/{canli}")
def benzer_canlilar(canli: str, limit: int = 5):
    try:
        oneriler = benzerlik_.oneriler_getir(canli,en_fazla=limit)
        return{
            "canli": canli,
            "oneri_sayisi": len(oneriler),
            "oneriler": oneriler
        }
    except Exception as e:
        print(f"Öneri hatası: {e}")
        return {
            "canli": canli,
            "oneri_sayisi": 0,
            "oneriler": []
        }


@app.get("/kimlik/{canli}")
def dijital_kimlik(canli: str):
    
    kayit = canli_getir(canli)
    
    if kayit:
        metin = kayit['tam_metin']
        baslik = kayit['baslik']
        kimlik = dijital_kimlik_olustur(baslik, metin)
        return kimlik
    
    canli_en = turkce_ingilizce_cevir(canli)
    
    veri = veri_cek(canli_en)
    if isinstance(veri, str):
        return {"hata": veri}
    
    birlesik_metin = veri['giris_ozeti'] + "\n\n" + veri['tam_metin']
    
    ozet = metni_ozetle(birlesik_metin, cumle_sayisi=15)
    canli_kaydet({
        'baslik': veri['baslik'],
        'giris_ozeti': veri['giris_ozeti'],
        'genel_ozet': ozet,
        'tam_metin': birlesik_metin,
        'url': veri['url']
    })
    
    kimlik = dijital_kimlik_olustur(veri['baslik'], birlesik_metin)
    return kimlik

@app.get("/", response_class=HTMLResponse)
def ana_sayfa():
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(html_path, "r", encoding="utf-8") as f: 
        return f.read()
    
@app.get("/ara")
def canli_ara(konu: str = Query(...)):

    kayitli = canli_getir(konu)
    if kayitli:
        return {
            "kaynak": "veritabanı",
            "baslik": kayitli['baslik'],
            "ozet": kayitli['genel_ozet'],
            "url": kayitli['url']
        }
    
    konu_en = turkce_ingilizce_cevir(konu)
    
    veri = veri_cek(konu_en)
    if isinstance(veri, str):
        return {"hata": veri}
    
    birlesik_metin = veri['giris_ozeti'] + "\n\n" + veri['tam_metin']
    ozet = metni_ozetle(birlesik_metin, cumle_sayisi=15)

    if len(ozet) < 200:
        ozet = veri['giris_ozeti']

    canli_kaydet({
        'baslik': veri['baslik'],
        'giris_ozeti': veri['giris_ozeti'],
        'genel_ozet': ozet,
        'tam_metin': birlesik_metin,
        'url': veri['url']
    })
    
    return {
        "kaynak": "wikipedia",
        "baslik": veri['baslik'],
        "ozet": ozet,
        "url": veri['url']
    }
    
@app.get("/liste")
def liste():
    baglanti = baglanti_kur()
    if not baglanti:
        return {"hata": "veri tabanı bağlantısı kurulmadı"}
    
    cursor = baglanti.cursor()
    cursor.execute("select baslik, url from canlinin_bilgileri")
    satirlar = cursor.fetchall()
    baglanti.close()

    return {"toplam": len(satirlar), "canlilar": [{"baslik": r[0], "url": r[1]} for r in satirlar]}

if __name__ == "__main__":
    import webbrowser
    import uvicorn
    webbrowser.open("http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")