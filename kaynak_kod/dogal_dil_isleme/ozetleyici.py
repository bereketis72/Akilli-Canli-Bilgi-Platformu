import re

def metni_ozetle(metin, dil="turkish", cumle_sayisi=15):
    cumleler = re.split(r'(?<=[.!?])\s+', metin)
    cumleler = [c.strip() for c in cumleler if len(c.strip()) > 20]
    secilen_cumleler = cumleler[:cumle_sayisi]
    
    if len(secilen_cumleler) < cumle_sayisi:
        print(f"uyarı: Sadece {len(secilen_cumleler)} cümle bulundu")
    
    return " ".join(secilen_cumleler)

if __name__ == "__main__":
    ornek = "Aslanlar ormanların kralıdır. Çok güçlü hayvanlardır."
    print("Özet:", metni_ozetle(ornek, cumle_sayisi=2))