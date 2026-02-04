import random
import time

class benzerlik:
    def __init__(self):
        self.canli_havuzu = {
            "Aslan": ("https://tr.wikipedia.org/wiki/Aslan", "Hayvan"),
            "Kaplan": ("https://tr.wikipedia.org/wiki/Kaplan", "Hayvan"),
            "Fil": ("https://tr.wikipedia.org/wiki/Fil", "Hayvan"),
            "Zürafa": ("https://tr.wikipedia.org/wiki/Zürafa", "Hayvan"),
            "Zebra": ("https://tr.wikipedia.org/wiki/Zebra", "Hayvan"),
            "Kutup Ayısı": ("https://tr.wikipedia.org/wiki/Kutup_ayısı", "Hayvan"),
            "Penguen": ("https://tr.wikipedia.org/wiki/Penguen", "Hayvan"),
            "Yunus": ("https://tr.wikipedia.org/wiki/Yunus", "Hayvan"),
            "Köpekbalığı": ("https://tr.wikipedia.org/wiki/Köpekbalığı", "Hayvan"),
            "Kartal": ("https://tr.wikipedia.org/wiki/Kartal", "Hayvan"),
            "Kelebek": ("https://tr.wikipedia.org/wiki/Kelebek", "Hayvan"),
            "Örümcek": ("https://tr.wikipedia.org/wiki/Örümcek", "Hayvan"),
            "Yılan": ("https://tr.wikipedia.org/wiki/Yılan", "Hayvan"),
            "Timsah": ("https://tr.wikipedia.org/wiki/Timsah", "Hayvan"),
            "Kurbağa": ("https://tr.wikipedia.org/wiki/Kurbağa", "Hayvan"),
            "Gül": ("https://tr.wikipedia.org/wiki/Gül", "Bitki"),
            "Ayçiçeği": ("https://tr.wikipedia.org/wiki/Ayçiçeği", "Bitki"),
            "Meşe": ("https://tr.wikipedia.org/wiki/Meşe", "Bitki"),
            "Bambu": ("https://tr.wikipedia.org/wiki/Bambu", "Bitki"),
            "Kaktüs": ("https://tr.wikipedia.org/wiki/Kaktüs", "Bitki"),
            "Orkide": ("https://tr.wikipedia.org/wiki/Orkide", "Bitki"),
            "Lale": ("https://tr.wikipedia.org/wiki/Lale", "Bitki"),
            "Çam": ("https://tr.wikipedia.org/wiki/Çam", "Bitki"),
            "Zambak": ("https://tr.wikipedia.org/wiki/Zambak", "Bitki"),
            "Çita": ("https://tr.wikipedia.org/wiki/Çita", "Hayvan"),
            "Leopar": ("https://tr.wikipedia.org/wiki/Leopar", "Hayvan"),
            "Panda": ("https://tr.wikipedia.org/wiki/Panda", "Hayvan"),
            "Kanguru": ("https://tr.wikipedia.org/wiki/Kanguru", "Hayvan"),
            "Koala": ("https://tr.wikipedia.org/wiki/Koala", "Hayvan"),
            "Kurt": ("https://tr.wikipedia.org/wiki/Kurt", "Hayvan"),
            "Tilki": ("https://tr.wikipedia.org/wiki/Tilki", "Hayvan"),
            "Geyik": ("https://tr.wikipedia.org/wiki/Geyik", "Hayvan"),
            "At": ("https://tr.wikipedia.org/wiki/At", "Hayvan"),
            "İnek": ("https://tr.wikipedia.org/wiki/İnek", "Hayvan"),
            "Tavuk": ("https://tr.wikipedia.org/wiki/Tavuk", "Hayvan"),
            "Ördek": ("https://tr.wikipedia.org/wiki/Ördek", "Hayvan"),
            "Baykuş": ("https://tr.wikipedia.org/wiki/Baykuş", "Hayvan"),
            "Papağan": ("https://tr.wikipedia.org/wiki/Papağan", "Hayvan"),
            "Flamingo": ("https://tr.wikipedia.org/wiki/Flamingo", "Hayvan"),
            "Gergedan": ("https://tr.wikipedia.org/wiki/Gergedan", "Hayvan"),
            "Su Aygırı": ("https://tr.wikipedia.org/wiki/Su_aygırı", "Hayvan"),
            "Balina": ("https://tr.wikipedia.org/wiki/Balina", "Hayvan"),
            "Ahtapot": ("https://tr.wikipedia.org/wiki/Ahtapot", "Hayvan"),
            "Deniz Yıldızı": ("https://tr.wikipedia.org/wiki/Deniz_yıldızı", "Hayvan")
        }
    
    def oneriler_getir(self, canli_baslik, en_fazla=5):
        random.seed(time.time())
        
        tum_canlilar = list(self.canli_havuzu.keys())
        
        
        filtreli = [c for c in tum_canlilar if c.lower() != canli_baslik.lower()]
        
        secilmis = random.sample(filtreli, min(en_fazla, len(filtreli)))
        
        oneriler = []
        for canli in secilmis:
            url, kategori = self.canli_havuzu[canli]
            oneriler.append({
                'baslik': canli,
                'kategori': kategori,
                'url': url
            })
        
        return oneriler