import pandas as pd
import re
import os

# ============================================================
#  AYARLAR
# ============================================================

DOSYA_1 = r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\1711-Final-Dataset.xlsx"
DOSYA_2 = r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\1711-Final-Test-Dataset.xlsx"

# Kaç örnek görmek istiyorsun? (gerçek veri içeriyorsa 2-3 yeterli)
ORNEK_SATIR_SAYISI = 5

# ============================================================
#  KOD
# ============================================================

def analiz_et(dosya_yolu):
    dosya_adi = os.path.basename(dosya_yolu)
    print(f"\n{'='*60}")
    print(f"📂 DOSYA: {dosya_adi}")
    print(f"{'='*60}")

    xls = pd.ExcelFile(dosya_yolu)
    print(f"📋 Sayfa sayısı : {len(xls.sheet_names)}")
    print(f"📋 Sayfalar     : {xls.sheet_names}")

    for sayfa in xls.sheet_names:
        df = pd.read_excel(dosya_yolu, sheet_name=sayfa)

        print(f"\n  ── Sayfa: '{sayfa}' ──")
        print(f"  Satır: {len(df)}  |  Sütun: {len(df.columns)}")
        print(f"\n  {'SÜTUN ADI':<30} {'TİP':<12} {'BOŞ SAYISI':<12} {'DOLU%'}")
        print(f"  {'-'*70}")

        for sutun in df.columns:
            tip    = str(df[sutun].dtype)
            bos    = df[sutun].isna().sum()
            dolu   = round((1 - bos / len(df)) * 100, 1) if len(df) > 0 else 0
            print(f"  {str(sutun):<30} {tip:<12} {bos:<12} {dolu}%")

        # Metin sütunları için örnek + karakter istatistiği
        metin_sutunlar = df.select_dtypes(include="object").columns.tolist()
        if metin_sutunlar:
            print(f"\n  📝 METİN SÜTUNLARI — İlk {ORNEK_SATIR_SAYISI} örnek ve istatistik:")
            for sutun in metin_sutunlar:
                ornekler = df[sutun].dropna().head(ORNEK_SATIR_SAYISI).tolist()
                dolu_df  = df[sutun].dropna().astype(str)
                if len(dolu_df) == 0:
                    continue
                ort_uzunluk = round(dolu_df.str.len().mean(), 1)
                max_uzunluk = dolu_df.str.len().max()
                min_uzunluk = dolu_df.str.len().min()

                print(f"\n  [{sutun}]")
                print(f"    Ort. karakter: {ort_uzunluk}  |  Min: {min_uzunluk}  |  Max: {max_uzunluk}")
                for i, ornek in enumerate(ornekler, 1):
                    # Uzun metinleri kırp
                    goster = ornek if len(ornek) <= 200 else ornek[:200] + "..."
                    print(f"    Örnek {i}: {goster}")

                # Yaygın önek/sonek kalıpları tespit et
                ilk_kelimeler = dolu_df.str.split().str[0].value_counts().head(5)
                print(f"    En sık başlangıç kelimeleri: {ilk_kelimeler.to_dict()}")

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    for dosya in [DOSYA_1, DOSYA_2]:
        if os.path.exists(dosya):
            analiz_et(dosya)
        else:
            print(f"\n⚠️  Dosya bulunamadı: {dosya}")
            print("   Lütfen dosya yolunu kontrol et.\n")

    print("✅ Analiz tamamlandı. Çıktıyı Claude'a yapıştırabilirsin.")