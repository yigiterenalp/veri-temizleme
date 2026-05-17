import pandas as pd
import os

# ============================================================
#  AYARLAR
# ============================================================

DOSYALAR = [
    {
        "parca1": r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\temizlenmis\1711-Final-Dataset_parca1_temiz.xlsx",
        "parca2": r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\temizlenmis\1711-Final-Dataset_parca2_temiz.xlsx",
        "cikti":  r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\temizlenmis\1711-Final-Dataset_temiz.xlsx",
    },
]

# ============================================================
#  BİRLEŞTİR VE DOĞRULA
# ============================================================

for d in DOSYALAR:
    p1_yol = d["parca1"]
    p2_yol = d["parca2"]
    cikti  = d["cikti"]

    if not os.path.exists(p1_yol):
        print(f"⚠️  Bulunamadı: {p1_yol}"); continue
    if not os.path.exists(p2_yol):
        print(f"⚠️  Bulunamadı: {p2_yol}"); continue

    df1 = pd.read_excel(p1_yol)
    df2 = pd.read_excel(p2_yol)

    print(f"\n{'='*60}")
    print(f"📂 {os.path.basename(cikti)}")
    print(f"{'='*60}")
    print(f"  parca1 : {len(df1)} satır  — sütunlar: {list(df1.columns)}")
    print(f"  parca2 : {len(df2)} satır  — sütunlar: {list(df2.columns)}")

    if list(df1.columns) != list(df2.columns):
        print(f"  ❌ SÜTUN ADLARI FARKLI — birleştirme iptal!")
        print(f"     parca1: {list(df1.columns)}")
        print(f"     parca2: {list(df2.columns)}")
        continue

    df = pd.concat([df1, df2], ignore_index=True)
    print(f"  Birleşik: {len(df)} satır  (beklenen: {len(df1)+len(df2)})")

    if len(df) != len(df1) + len(df2):
        print(f"  ❌ SATIR SAYISI UYUŞMUYOR!")
        continue

    df.to_excel(cikti, index=False)
    print(f"  ✅ Kaydedildi: {cikti}")

print(f"\n✅ Tamamlandı.")