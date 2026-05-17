import pandas as pd
import os

# ============================================================
#  AYARLAR
# ============================================================

DOSYALAR = [
    r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\1711-Final-Dataset.xlsx",
    r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\1711-Final-Test-Dataset.xlsx",
]

CIKTI_KLASORU = r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\bolunmus"

# ============================================================
#  KOD
# ============================================================

os.makedirs(CIKTI_KLASORU, exist_ok=True)

for dosya_yolu in DOSYALAR:
    if not os.path.exists(dosya_yolu):
        print(f"⚠️  Bulunamadı, atlandı: {dosya_yolu}")
        continue

    dosya_adi = os.path.basename(dosya_yolu)
    kok_ad    = os.path.splitext(dosya_adi)[0]

    df = pd.read_excel(dosya_yolu)
    toplam = len(df)
    orta   = toplam // 2

    parca_1 = df.iloc[:orta].reset_index(drop=True)
    parca_2 = df.iloc[orta:].reset_index(drop=True)

    yol_1 = os.path.join(CIKTI_KLASORU, f"{kok_ad}_parca1.xlsx")
    yol_2 = os.path.join(CIKTI_KLASORU, f"{kok_ad}_parca2.xlsx")

    parca_1.to_excel(yol_1, index=False)
    parca_2.to_excel(yol_2, index=False)

    print(f"\n📂 {dosya_adi}  ({toplam} satır)")
    print(f"   ✅ parca1 → {orta} satır      → {yol_1}")
    print(f"   ✅ parca2 → {toplam - orta} satır      → {yol_2}")

print("\n✅ Bölme tamamlandı.")