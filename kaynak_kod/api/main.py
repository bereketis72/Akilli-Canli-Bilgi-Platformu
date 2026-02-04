import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from veri_kaynaklari.wikipedia import veri_cek
from dogal_dil_isleme.ozetleyici import metni_ozetle
from veritabani.db import canli_getir, canli_kaydet

def ana_main():
    konu = input("hakkında bilgi almak istediğiniz canlı nedir? ").strip()
    if not konu:
        print("geçerli bir canlı ismi giriniz")
        return

    print(f"\n '{konu}' canlısı için arama başlatılıyor")
    kayitli_veri = canli_getir(konu)
    
    if kayitli_veri:
        print("Aradığınız canlı veritabanında bulundu! (Hızlı Erişim)")
        final_baslik = kayitli_veri['baslik']
        final_ozet = kayitli_veri['genel_ozet']
        final_url = kayitli_veri['url']
    else:
        print("Database'de bulunamadı, Wikipedia'dan çekiliyor...")
        veri = veri_cek(konu)
    
        if isinstance(veri, str):
            print(f"hata: {veri}")
            return
        
      
        final_ozet = metni_ozetle(veri['tam_metin'], cumle_sayisi=5)
        final_baslik = veri['baslik']
        final_url = veri['url']

 
        yeni_kayit = {
            'baslik': final_baslik,
            'giris_ozeti': veri['giris_ozeti'],
            'genel_ozet': final_ozet,
            'tam_metin': veri['tam_metin'],
            'url': final_url
        }
        canli_kaydet(yeni_kayit)

    print(f"\nBAŞLIK: {final_baslik}")
    print(f"Web Adresi: {final_url}")
    print(f"GENEL ÖZET:\n{final_ozet}")
    print("\n" + "*"*20)

if __name__ == "__main__":
    ana_main()