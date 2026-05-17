import pandas as pd
import os

# ============================================================
#  AYARLAR
# ============================================================

DOSYA_CIFTLERI = [
    {
        "orijinal": r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\bolunmus\1711-Final-Dataset_parca1.xlsx",
        "temiz":    r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\temizlenmis\1711-Final-Dataset_parca1_temiz.xlsx",
    },
    {
        "orijinal": r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\bolunmus\1711-Final-Test-Dataset_parca1.xlsx",
        "temiz":    r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\temizlenmis\1711-Final-Test-Dataset_parca1_temiz.xlsx",
    },
]

DOKUNULMAYAN_SUTUNLAR = ["id", "kategori", "doc_id"]
TEMIZLENEN_SUTUNLAR   = ["soru", "cevap"]

# Kaç karakter altındaki temizlenmiş metin şüpheli sayılsın?
MIN_KARAKTER_ESIGI = 10

# Hiç değişmeyen satırları kaç tane gösterelim?
DEGISMEYEN_ORNEK = 10

# Şüpheli satırları kaç tane gösterelim?
SUPHELI_ORNEK = 20

# ============================================================
#  KONTROL FONKSİYONLARI
# ============================================================

def sutun_kayma_kontrol(df_ori, df_tem, dosya_adi):
    print(f"\n{'─'*65}")
    print(f"[1] SÜTUN KAYMASI / BOZULMA KONTROLÜ — {dosya_adi}")
    print(f"{'─'*65}")

    # Satır sayısı eşleşiyor mu?
    if len(df_ori) != len(df_tem):
        print(f"  ❌ SATIR SAYISI FARKLI! Orijinal: {len(df_ori)}  Temiz: {len(df_tem)}")
    else:
        print(f"  ✅ Satır sayısı eşleşiyor: {len(df_ori)}")

    # Sütun adları aynı mı?
    if list(df_ori.columns) != list(df_tem.columns):
        print(f"  ❌ SÜTUN ADLARI FARKLI!")
        print(f"     Orijinal : {list(df_ori.columns)}")
        print(f"     Temiz    : {list(df_tem.columns)}")
    else:
        print(f"  ✅ Sütun adları eşleşiyor: {list(df_ori.columns)}")

    # Dokunulmayan sütunlar birebir aynı mı?
    for sutun in DOKUNULMAYAN_SUTUNLAR:
        if sutun not in df_ori.columns:
            continue
        eslesmeyen = (df_ori[sutun] != df_tem[sutun]).sum()
        if eslesmeyen > 0:
            print(f"  ❌ '{sutun}' sütununda {eslesmeyen} satır farklı — KAYME VAR!")
            print(df_ori[df_ori[sutun] != df_tem[sutun]][sutun].head(5).to_string())
        else:
            print(f"  ✅ '{sutun}' sütunu birebir aynı — kayma yok")


def degismeyen_satir_kontrol(df_ori, df_tem, dosya_adi):
    print(f"\n{'─'*65}")
    print(f"[2] HİÇ DEĞİŞMEYEN SATIRLAR — {dosya_adi}")
    print(f"{'─'*65}")

    for sutun in TEMIZLENEN_SUTUNLAR:
        if sutun not in df_ori.columns:
            continue
        mask = df_ori[sutun].notna() & (df_ori[sutun] == df_tem[sutun])
        sayi = mask.sum()
        print(f"\n  [{sutun}] Değişmeyen: {sayi} / {len(df_ori)} satır")
        if sayi > 0:
            ornekler = df_ori[mask][sutun].head(DEGISMEYEN_ORNEK)
            for i, metin in enumerate(ornekler, 1):
                print(f"    {i}. {str(metin)[:120]}")


def supheli_satir_kontrol(df_ori, df_tem, dosya_adi):
    print(f"\n{'─'*65}")
    print(f"[3] ŞÜPHELİ DEĞİŞİMLER — {dosya_adi}")
    print(f"{'─'*65}")

    for sutun in TEMIZLENEN_SUTUNLAR:
        if sutun not in df_tem.columns:
            continue

        supheli = []

        for i in range(len(df_tem)):
            ori = str(df_ori[sutun].iloc[i]) if pd.notna(df_ori[sutun].iloc[i]) else ""
            tem = str(df_tem[sutun].iloc[i]) if pd.notna(df_tem[sutun].iloc[i]) else ""

            # Boş kalan
            if ori and not tem.strip():
                supheli.append((i, "BOŞ KALDI", ori, tem))
            # Çok kısa kalan (orijinali uzundu ama temizi çok kısa)
            elif len(ori) > 30 and len(tem) < MIN_KARAKTER_ESIGI:
                supheli.append((i, "ÇOK KISA KALDI", ori, tem))
            # Aşırı kısalma (orijinalin %20'sinden azı kaldı)
            elif len(ori) > 50 and len(tem) < len(ori) * 0.2:
                supheli.append((i, f"AŞIRI KISALDI ({len(ori)}→{len(tem)} karakter)", ori, tem))

        print(f"\n  [{sutun}] Şüpheli: {len(supheli)} satır")
        for idx, tip, ori, tem in supheli[:SUPHELI_ORNEK]:
            print(f"\n    Satır {idx+1} — {tip}")
            print(f"    ÖNCE : {ori[:150]}")
            print(f"    SONRA: {tem[:150]}")

        if len(supheli) > SUPHELI_ORNEK:
            print(f"\n    ... ve {len(supheli) - SUPHELI_ORNEK} satır daha")


def genel_istatistik(df_ori, df_tem, dosya_adi):
    print(f"\n{'─'*65}")
    print(f"[4] GENEL İSTATİSTİK — {dosya_adi}")
    print(f"{'─'*65}")

    for sutun in TEMIZLENEN_SUTUNLAR:
        if sutun not in df_ori.columns:
            continue
        ori_len = df_ori[sutun].dropna().astype(str).str.len()
        tem_len = df_tem[sutun].dropna().astype(str).str.len()
        degisen = (df_ori[sutun] != df_tem[sutun]).sum()

        print(f"\n  [{sutun}]")
        print(f"    Değişen satır    : {degisen} / {len(df_ori)}")
        print(f"    Ort. karakter    : {ori_len.mean():.1f} → {tem_len.mean():.1f}")
        print(f"    Toplam karakter  : {ori_len.sum()} → {tem_len.sum()} "
              f"({'+' if tem_len.sum() > ori_len.sum() else ''}{tem_len.sum()-ori_len.sum()} fark)")


# ============================================================
#  ÇALIŞTIR
# ============================================================

if __name__ == "__main__":
    for cift in DOSYA_CIFTLERI:
        ori_yol = cift["orijinal"]
        tem_yol = cift["temiz"]
        dosya_adi = os.path.basename(tem_yol)

        if not os.path.exists(ori_yol):
            print(f"\n⚠️  Orijinal bulunamadı: {ori_yol}")
            continue
        if not os.path.exists(tem_yol):
            print(f"\n⚠️  Temiz bulunamadı: {tem_yol}")
            continue

        df_ori = pd.read_excel(ori_yol)
        df_tem = pd.read_excel(tem_yol)

        print(f"\n{'='*65}")
        print(f"KONTROL: {dosya_adi}")
        print(f"{'='*65}")

        sutun_kayma_kontrol(df_ori, df_tem, dosya_adi)
        degismeyen_satir_kontrol(df_ori, df_tem, dosya_adi)
        supheli_satir_kontrol(df_ori, df_tem, dosya_adi)
        genel_istatistik(df_ori, df_tem, dosya_adi)

    print(f"\n{'='*65}")
    print("✅ Kontrol tamamlandı.")
    print(f"{'='*65}")