import pandas as pd
import re
import os

# ============================================================
#  AYARLAR
# ============================================================

DOSYALAR = [
    r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\bolunmus\1711-Final-Dataset_parca1.xlsx",
    r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\bolunmus\1711-Final-Test-Dataset_parca1.xlsx",
]

CIKTI_KLASORU = r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\temizlenmis"
TEMIZLENECEK_SUTUNLAR = ["soru", "cevap"]

MODEL_KODLARI = [
    "BMSO", "BMSY", "BMDO", "BMDY", "BMSS",
    "CDGH", "CDGS", "DGH", "DGS", "CGH", "CGS", "CDS",
    "DG", "GS", "GA", "NC", "XS", "CS", "GLS", "GH",
    "CNC", "BMS", "MANUAL",
]

EKLER = [
    "makinelerinde", "makinelerinin", "makinelerine", "makinelerde",
    "makinelerdeki", "makinelerin", "makinenin", "makineler", "makine",
    "makinesinde", "makinede", "makinesinin", "makinesi için", "makinası için",
    "makinalarda", "makinalarında", "makinaların", "makinanın",
    "modellerinde", "modelinde",
    "model makinede", "model makinelerinde", "model makinelerde",
    "model makinada", "model makinalarda",
]

# ============================================================
#  REGEX DERLEME
# ============================================================

def _pattern_derle():
    kodlar = "|".join(sorted(MODEL_KODLARI, key=len, reverse=True))
    ekler  = "|".join(sorted(EKLER, key=len, reverse=True))

    # Tek token: bilinen kod (+ opsiyonel sayı/harf suffix) VEYA tek büyük harf
    token  = r"(?:(?:" + kodlar + r")(?:\s+[\w\d]+)?|[A-Z])"
    # Ayraç: virgül, slash, boşluk, ve/ile
    ayrac  = r"(?:\s*[,/]\s*|\s+(?:ve|ile)\s+|\s+)"
    # Kod bloğu: bir veya daha fazla token + aralarında ayraç veya bilinmeyen kelimeler
    blok   = (
        r"(?:" + token + r")"
        r"(?:" + ayrac + r"(?:" + token + r"|[\w]+))*"
        r"(?:\s*\.\.\.)?"
    )
    # makine* ile başlayan her türlü ek (makinesi, makinesinin, makinelerde vb.)
    mek    = r"makine(?:ler\w+|nin|de|si\w*|ye|yi|ler)(?:\s+i[çc]in)?"

    # Pattern 1: cümle başındaki kod bloğu + ek
    p_bas  = re.compile(
        r"^" + r"(?:" + blok + r")" +
        r"\s+(?:(?:Makine|MODEL|model)\s+)?" +
        r"(?:" + ekler + r"|" + mek + r")" +
        r"\s*",
        re.IGNORECASE
    )
    # Pattern 2: cümle başında tek başına "Makinelerde/Makinede" vb.
    p_tek  = re.compile(
        r"^(?:" + ekler + r")\s+",
        re.IGNORECASE
    )
    # Pattern 3: "yaşanan/bulunan/olan/tespit edilen [liste]... makine eki"
    tetik  = r"(?:yaşanan|bulunan|olan|tespit edilen)"
    p_orta = re.compile(
        tetik + r"\s+.{1,80}?\.\.\.\s*(?:" + ekler + r"|" + mek + r")\s*",
        re.IGNORECASE
    )
    return p_bas, p_tek, p_orta

P_BAS, P_TEK, P_ORTA = _pattern_derle()


def temizle(metin):
    if not isinstance(metin, str):
        return metin

    metin = P_BAS.sub("", metin).strip()
    metin = P_TEK.sub("", metin).strip()
    metin = P_ORTA.sub(r" ", metin).strip()
    metin = re.sub(r" {2,}", " ", metin).strip()

    if metin:
        metin = metin[0].upper() + metin[1:]

    return metin


# ============================================================
#  ÖNİZLEME
# ============================================================

def onizleme(dosya_yolu, n=5):
    df = pd.read_excel(dosya_yolu)
    print(f"\n{'='*65}")
    print(f"ÖNİZLEME: {os.path.basename(dosya_yolu)}")
    print(f"{'='*65}")
    for sutun in TEMIZLENECEK_SUTUNLAR:
        if sutun not in df.columns:
            continue
        print(f"\n--- {sutun.upper()} ---")
        for i, metin in enumerate(df[sutun].dropna().head(n), 1):
            sonuc = temizle(metin)
            if metin != sonuc:
                print(f"\n  [{i}] ÖNCE : {metin[:150]}")
                print(f"  [{i}] SONRA: {sonuc[:150]}")
            else:
                print(f"\n  [{i}] DEĞİŞMEDİ: {metin[:150]}")


# ============================================================
#  ANA İŞLEM
# ============================================================

def isle(dosya_yolu):
    df = pd.read_excel(dosya_yolu)
    dosya_adi = os.path.basename(dosya_yolu)
    kok_ad    = os.path.splitext(dosya_adi)[0]

    degisen_toplam = 0
    for sutun in TEMIZLENECEK_SUTUNLAR:
        if sutun not in df.columns:
            print(f"  ⚠️  '{sutun}' bulunamadı, atlandı.")
            continue
        onceki    = df[sutun].copy()
        df[sutun] = df[sutun].apply(temizle)
        degisen   = (df[sutun] != onceki).sum()
        degisen_toplam += degisen
        print(f"  ✅ {sutun}: {degisen} satır değişti")

    os.makedirs(CIKTI_KLASORU, exist_ok=True)
    cikti = os.path.join(CIKTI_KLASORU, f"{kok_ad}_temiz.xlsx")
    df.to_excel(cikti, index=False)
    print(f"  💾 Kaydedildi: {cikti}")
    print(f"  📊 Toplam değişen: {degisen_toplam} / {len(df)} satır")


# ============================================================
#  ÇALIŞTIR
# ============================================================

if __name__ == "__main__":

    # ADIM 1 — Önizlemeye bak
    for dosya in DOSYALAR:
        if os.path.exists(dosya):
            onizleme(dosya)
        else:
            print(f"\n⚠️  Bulunamadı: {dosya}")

    # ADIM 2 — Önizleme tamam görünüyorsa aşağıdaki # işaretlerini kaldır
    print("\n" + "="*65)
    print("TEMİZLEME BAŞLIYOR")
    print("="*65)
    for dosya in DOSYALAR:
        if os.path.exists(dosya):
            print(f"\n📂 {os.path.basename(dosya)}")
            isle(dosya)
    print("\n✅ Tamamlandı.")