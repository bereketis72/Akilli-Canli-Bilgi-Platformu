import re 

def dijital_kimlik_olustur(baslik, metin):
    metin_lower = metin.lower()
    
    kimlik = {
        "baslik": baslik,
        "bilimsel_adi": bilimsel_ad_bul(metin),
        "familya": familya_bul(metin, baslik),
        "habitat": habitat_bul(metin),
        "beslenme": beslenme_bul(metin, baslik),
        "tehdit_durumu": tehdit_durumu_bul(metin),
        "ilginc_bilgi": ilginc_bilgi_bul(metin)
    }
    return kimlik

def bilimsel_ad_bul(metin):
    pattern = r'\(([A-Z][a-z]+ [a-z]+)\)'
    match = re.search(pattern, metin)
    if match:
        return match.group(1)
    pattern2 = r'bilimsel ad[ıi][:\s]+([A-Z][a-z]+ [a-z]+)'
    match2 = re.search(pattern2, metin, re.IGNORECASE)
    if match2:
        return match2.group(1)
    
    return ""

def familya_bul(metin, baslik=""):
    familyalar = {
        "Felidae": "Kedigiller",
        "Canidae": "Köpekgiller",
        "Ursidae": "Ayıgiller",
        "Elephantidae": "Filgiller",
        "Rosaceae": "Gülgiller",
        "Liliaceae": "Zambakgiller",
        "Poaceae": "Buğdaygiller",
        "Spheniscidae": "Penguengiller",
        "Bovidae": "Boynuzlugiller",
        "Equidae": "Atgiller",
        "Cervidae": "Geyikgiller",
        "Accipitridae": "Kartallar",
        "Delphinidae": "Yunusgiller",
        "Salmonidae": "Alabalıkgiller"
    }
    
    metin_lower = metin.lower()
    baslik_lower = baslik.lower()
    
    
    for latince, turkce in familyalar.items():
        if latince.lower() in metin_lower: 
            return f"{turkce} ({latince})"
    
    
    family_pattern = r'family[:\s]+(\w+idae|\w+aceae)'
    match = re.search(family_pattern, metin, re.IGNORECASE)
    if match:
        family_name = match.group(1)
        if family_name in familyalar:
            return f"{familyalar[family_name]} ({family_name})"
        return family_name
    
    if any(k in baslik_lower for k in ['panthera', 'leopar', 'aslan', 'kaplan', 'cheetah', 'çita']):
        return "Kedigiller (Felidae)"
    elif any(k in baslik_lower for k in ['wolf', 'fox', 'dog', 'kurt', 'tilki', 'köpek']):
        return "Köpekgiller (Canidae)"
    elif any(k in baslik_lower for k in ['bear', 'ayı']):
        return "Ayıgiller (Ursidae)"
    
    
    turkce_aramalar = {
        "kedigil": "Kedigiller (Felidae)",
        "köpekgil": "Köpekgiller (Canidae)",
        "penguengil": "Penguengiller (Spheniscidae)",
        "gülgil": "Gülgiller (Rosaceae)",
        "papatyagil": "Papatyagiller (Asteraceae)"
    }
    
    for arama, sonuc in turkce_aramalar.items():
        if arama in metin_lower:
            return sonuc
    
    return "Bilinmiyor"
    
        

def habitat_bul(metin):
    bolgeler = []  
    
    kitalar = {
        "africa": "Afrika", "afrika": "Afrika",
        "asia": "Asya", "asya": "Asya",
        "europe": "Avrupa", "avrupa": "Avrupa",
        "america": "Amerika", "amerika": "Amerika",
        "australia": "Avustralya", "avustralya": "Avustralya",
        "antarctica": "Antarktika", "antarktika": "Antarktika"
    }
    
    kutup_bölgeleri = {
        "arctic": "Arktik", "arktik": "Arktik", "kuzey kutbu": "Arktik",
        "antarctic": "Antarktik", "antarktik": "Antarktik", "güney kutbu": "Antarktik",
        "polar": "Kutup", "kutup": "Kutup"
    }
    
    kitalar = {
        "africa": "Afrika", "afrika": "Afrika",
        "asia": "Asya", "asya": "Asya",
        "europe": "Avrupa", "avrupa": "Avrupa",
        "america": "Amerika", "amerika": "Amerika",
        "australia": "Avustralya", "avustralya": "Avustralya",
        "antarctica": "Antarktika", "antarktika": "Antarktika"
    }
    
    ortamlar = {
        "forest": "Orman", "orman": "Orman",
        "savanna": "Savan", "savan": "Savan",
        "desert": "Çöl", "çöl": "Çöl",
        "ocean": "Okyanus", "okyanus": "Okyanus",
        "sea": "Deniz", "deniz": "Deniz",
        "lake": "Göl", "göl": "Göl",
        "mountain": "Dağ", "dağ": "Dağ",
        "grassland": "Step", "step": "Step"
    }
    
    metin_lower = metin.lower()
    
    for kelime, bolge in kutup_bölgeleri.items():
        if kelime in metin_lower and bolge not in bolgeler:
            bolgeler.append(bolge)
    
    for kelime, bolge in kitalar.items():
        if kelime in metin_lower and bolge not in bolgeler:
            bolgeler.append(bolge)
    
    for kelime, ortam in ortamlar.items():
        if kelime in metin_lower and ortam not in bolgeler:
            bolgeler.append(ortam)
    
    return ", ".join(bolgeler[:3]) if bolgeler else "Bilinmiyor"


def beslenme_bul(metin, baslik=""):
    metin_lower = metin.lower()
    baslik_lower = baslik.lower()
    
    
    etobur_genel = any(k in metin_lower for k in [
        "carnivore", "carnivorous", "predator", "hunt", "meat-eater", "meat eater", 
        "prey on", "feeds on animals", "eats meat", "hunting", "kills", "apex predator",
        "etobur", "etçil", "avlanır", "avlar", "av yapar", "et yer"
    ])
    
    etobur_spesifik = any(k in baslik_lower for k in [
        "panthera", "leopard", "tiger", "lion", "cheetah", "leopar", "aslan", "kaplan", "çita"
    ])
    
    if etobur_genel or etobur_spesifik:
        return "Etobur"
    
    
    elif any(k in metin_lower for k in [
        "herbivore", "herbivorous", "plant-eater", "plant eater", "vegetation", 
        "feeds on plants", "eats plants", "eats grass", "eats leaves", 
        "grazer", "browser", "folivore",
        "otobur", "otçül", "ot yer", "yaprak yer", "bitki yer", "ot ile beslenir"
    ]):
        return "Otobur"
    
    
    elif any(k in metin_lower for k in [
        "omnivore", "omnivorous", "both plants and animals",
        "hepçil", "her şey yer", "bitki ve hayvan"
    ]):
        return "Hepçil"
    
    
    elif any(k in metin_lower for k in [
        "photosynthesis", "photosynthe", "chlorophyll", "sunlight",
        "fotosentez", "klorofil"
    ]):
        return "Fotosentez"
    
    
    elif any(k in metin_lower for k in [
        "seed", "fruit", "berry", "nectar", "pollen",
        "tohum", "meyve", "çiçek", "polen", "nektar"
    ]):
        return "Tohumcul/Meyvecil"
    
    return "Bilinmiyor"

def tehdit_durumu_bul(metin):
    metin_lower = metin.lower()
    
    if any(k in metin_lower for k in ["critically endangered", "kritik tehlike", "nesli tükenmek"]):
        return "Kritik Tehlikede"
    elif any(k in metin_lower for k in ["endangered", "tehlike altında", "tehdit altında"]):
        return "Tehlikede"
    elif any(k in metin_lower for k in ["vulnerable", "hassas", "duyarlı"]):
        return "Hassas"
    elif any(k in metin_lower for k in ["near threatened", "koruma altında"]):
        return "Koruma Altında"
    elif any(k in metin_lower for k in ["least concern", "düşük risk"]):
        return "Düşük Risk"
    
    return "Değerlendirilmedi"

def ilginc_bilgi_bul(metin):
    cumleler = metin.replace('!', '.').replace('?', '.').split('.')
    
    ilginc_kaliplar = [
        "largest", "smallest", "fastest", "slowest", "only", "unique",
        "en büyük", "en küçük", "en hızlı", "en yavaş", "tek", "sadece",
        "can grow", "can reach", "up to", "metre", "kilogram", "years"
    ]
    
    for cumle in cumleler:
        cumle = cumle.strip()
        if len(cumle) > 30 and len(cumle) < 250:
            for kalip in ilginc_kaliplar:
                if kalip in cumle.lower():
                    return cumle + "."
    
    for cumle in cumleler:
        cumle = cumle.strip()
        if len(cumle) > 50 and len(cumle) < 250:
            return cumle + "."
    
    return "Bu konu hakkında ilginç bilgiler keşfediliyor..."