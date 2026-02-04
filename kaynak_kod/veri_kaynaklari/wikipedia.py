import wikipediaapi
from deep_translator import GoogleTranslator
import requests

def veri_cek(konu, dil="en"):  
    wiki = wikipediaapi.Wikipedia( 
        language = dil,
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent="bilgi platformu /1.0 (ornek@eposta.com)" 
    )

    sayfa = wiki.page(konu)
    if not sayfa.exists():
        return f"üzgünüm, '{konu}' başlığı altında bir içerik bulunamadı"

    try:
        translator = GoogleTranslator(source='en', target='tr')
        
        def cevir_parcala(metin, max_uzunluk=4000):
            if len(metin) <= max_uzunluk:
                return translator.translate(metin)
            
            cumleler = metin.split('. ')
            cevrilen = []
            gecici = ""
            
            for cumle in cumleler:
                if len(gecici) + len(cumle) < max_uzunluk:
                    gecici += cumle + ". "
                else:
                    if gecici:
                        cevrilen.append(translator.translate(gecici))
                    gecici = cumle + ". "
            
            if gecici:
                cevrilen.append(translator.translate(gecici))
            
            return " ".join(cevrilen)
        
        tam_metin_tr = cevir_parcala(sayfa.text[:8000])
        giris_ozeti_tr = cevir_parcala(sayfa.summary[:2000])
        baslik_tr = translator.translate(sayfa.title)
    except Exception as e:
        print(f"Çeviri hatası: {e}")
        tam_metin_tr = sayfa.text
        giris_ozeti_tr = sayfa.summary
        baslik_tr = sayfa.title
    
    if any(check in sayfa.title.lower() for check in ['(disambiguation)', 'disambiguation']):
        return f"'{konu}' bir anlam ayrımı sayfası, lütfen daha spesifik bir terim deneyin"
    
    summary_start = sayfa.summary[:200].lower()
    if any(phrase in summary_start for phrase in [
        'may refer to:', 'anlamlara gelebilir', 'can refer to'
    ]):
        return f"'{konu}' birden fazla anlama geliyor, lütfen daha spesifik olun"
    
    return {
        "baslik": baslik_tr,
        "giris_ozeti": giris_ozeti_tr,
        "tam_metin": tam_metin_tr,
        "url": sayfa.fullurl
    }

def ingilizce_turkce_cevir(kelime):
    pass



if __name__ == "__main__":
    aranacak_kelime = input("hangi hayvan veya bitikiyi merak ediyorsunuz ? ")
    sonuc = veri_cek(aranacak_kelime)
    if isinstance(sonuc, dict):
        print(f"\n bulunan başlık: {sonuc['baslik']}")
        print(f"Wikipedia linki {sonuc['url']}")
    else:
        print(sonuc)


        