import pandas as pd
import re
import os

# ============================================================
#  AYARLAR
# ============================================================

DOSYA = r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\temizlenmis\1711-Final-Test-Dataset_temiz.xlsx"
CIKTI = r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\temizlenmis\1711-Final-Test-Dataset_temiz_v2.xlsx"

TEMIZLENECEK_SUTUNLAR = ["test_sorgusu", "soru", "cevap"]

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

    token  = r"(?:(?:" + kodlar + r")(?:\s+[\w\d]+)?|[A-Z])"
    ayrac  = r"(?:\s*[,/]\s*|\s+(?:ve|ile)\s+|\s+)"
    blok   = (
        r"(?:" + token + r")"
        r"(?:" + ayrac + r"(?:" + token + r"|[A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜ0-9]*))*"
        r"(?:\s*\.\.\.)?"
    )
    mek    = r"makine(?:ler\w+|nin|de|si\w*|ye|yi|ler)(?:\s+i[çc]in)?"

    p_bas  = re.compile(
        r"^" + r"(?:" + blok + r")" +
        r"\s+(?:(?:Makine|MODEL|model)\s+)?" +
        r"(?:" + ekler + r"|" + mek + r")" +
        r"\s*",
        re.IGNORECASE
    )
    ekler_tek = "|".join(sorted([e for e in EKLER if not e.startswith("model")], key=len, reverse=True))
    p_tek  = re.compile(r"^(?:" + ekler_tek + r")\s+", re.IGNORECASE)

    tetik  = r"(?:yaşanan|bulunan|olan|tespit edilen)"
    p_orta = re.compile(
        tetik + r"\s+.{1,80}?\.\.\.\s*(?:" + ekler + r"|" + mek + r")\s*",
        re.IGNORECASE
    )
    return p_bas, p_tek, p_orta

P_BAS, P_TEK, P_ORTA = _pattern_derle()

# test_sorgusu sütunu için özel pattern
def _sorgu_pattern_derle():
    kodlar = "|".join(sorted(MODEL_KODLARI, key=len, reverse=True))
    apstr  = r"['\u2018\u2019][a-z\u00fc\u00e7\u011f\u0131\u015f\u00f6A-Z\u00dc\u00c7\u011e\u0130\u015e\u00d6]+"
    ayrac  = r"(?:\s*[,/]\s*|\s+(?:ve|ile)\s+|\s+)"
    token  = r"(?:(?:" + kodlar + r")(?:" + apstr + r"|(?:\s+[\w\d]+))?)"
    blok   = r"(?:" + token + r")(?:" + ayrac + r"(?:" + token + r"))*(?:\s*\.\.\.)?"

    # Cümle başında kod bloğu + ardından gelen ilk küçük harfe kadar sil
    p = re.compile(
        r"^(?:" + blok + r")\s+",
        re.IGNORECASE
    )
    p_bagli   = re.compile(r"^(?:ve|ile)\s+", re.IGNORECASE)
    p_kalinti = re.compile(r"^(?:için|si)\s*[,.]?\s*", re.IGNORECASE)
    return p, p_bagli, p_kalinti

P_SORGU, P_BAGLI, P_KALINTI_SORGU = _sorgu_pattern_derle()


def temizle_sorgu(metin):
    if not isinstance(metin, str): return metin
    m = P_SORGU.match(metin)
    if m:
        metin = metin[m.end():].strip()
    metin = P_BAGLI.sub("", metin).strip()
    metin = re.sub(r" {2,}", " ", metin).strip()
    if metin: metin = metin[0].upper() + metin[1:]
    return metin


def temizle_soru_kalinti(metin):
    if not isinstance(metin, str): return metin
    metin = P_KALINTI_SORGU.sub("", metin).strip()
    if metin: metin = metin[0].upper() + metin[1:]
    return metin


def temizle(metin, sutun=None):
    if not isinstance(metin, str):
        return metin
    if sutun == "test_sorgusu":
        return temizle_sorgu(metin)
    if sutun in ("soru", "cevap"):
        return temizle_soru_kalinti(temizle(metin))

    # Apostrof + hal eki: "BMSO'da", "BMSY'de", "DG'de" vb. → cümle başında sil
    kodlar_re = "|".join(sorted(MODEL_KODLARI, key=len, reverse=True))
    metin = re.sub(
        r"^(?:(?:" + kodlar_re + r")['''][a-züçğışöA-ZÜÇĞİŞÖ]+\s+)+",
        "", metin, flags=re.IGNORECASE
    ).strip()

    metin = P_BAS.sub("", metin).strip()
    metin = P_TEK.sub("", metin).strip()
    metin = P_ORTA.sub(" ", metin).strip()
    metin = re.sub(r" {2,}", " ", metin).strip()
    if metin:
        metin = metin[0].upper() + metin[1:]
    return metin


# ============================================================
#  ÖNİZLEME
# ============================================================

def onizleme(n=20):
    df = pd.read_excel(DOSYA)
    print(f"\n{'='*65}")
    print(f"ÖNİZLEME: {os.path.basename(DOSYA)}")
    print(f"Toplam satır: {len(df)}  |  Sütunlar: {list(df.columns)}")
    print(f"{'='*65}")
    for sutun in TEMIZLENECEK_SUTUNLAR:
        if sutun not in df.columns:
            print(f"\n  ⚠️  '{sutun}' sütunu bulunamadı")
            continue
        print(f"\n--- {sutun.upper()} ---")
        for i, metin in enumerate(df[sutun].dropna().head(n), 1):
            sonuc = temizle(metin, sutun=sutun)
            if metin != sonuc:
                print(f"\n  [{i}] ÖNCE : {str(metin)[:150]}")
                print(f"  [{i}] SONRA: {sonuc[:150]}")
            else:
                print(f"\n  [{i}] DEĞİŞMEDİ: {str(metin)[:150]}")


# ============================================================
#  ANA İŞLEM
# ============================================================

def isle():
    df = pd.read_excel(DOSYA)
    degisen_toplam = 0
    for sutun in TEMIZLENECEK_SUTUNLAR:
        if sutun not in df.columns:
            print(f"  ⚠️  '{sutun}' bulunamadı, atlandı.")
            continue
        onceki    = df[sutun].copy()
        df[sutun] = df[sutun].apply(lambda x: temizle(x, sutun=sutun))
        degisen   = (df[sutun] != onceki).sum()
        degisen_toplam += degisen
        print(f"  ✅ {sutun}: {degisen} satır değişti")

    df.to_excel(CIKTI, index=False)
    print(f"  💾 Kaydedildi: {CIKTI}")
    print(f"  📊 Toplam değişen: {degisen_toplam} / {len(df)} satır")


# ============================================================
#  ÇALIŞTIR
# ============================================================

if __name__ == "__main__":

    # ADIM 1 — Önizlemeye bak
    onizleme()

    # ADIM 2 — Önizleme tamam görünüyorsa aşağıdaki # işaretlerini kaldır
    print("\n" + "="*65)
    print("TEMİZLEME BAŞLIYOR")
    print("="*65)
    isle()
    print("\n✅ Tamamlandı.")