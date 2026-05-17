import pandas as pd
import os

# ============================================================
#  AYARLAR
# ============================================================

ORIJINAL = r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\temizlenmis\1711-Final-Test-Dataset_temiz.xlsx"
TEMIZ    = r"C:\Users\yigit\OneDrive\Desktop\veri temizleme\temizlenmis\1711-Final-Test-Dataset_temiz_v2.xlsx"

DOKUNULMAYAN_SUTUNLAR = ["doc_id", "id", "kategori"]
TEMIZLENEN_SUTUNLAR   = ["test_sorgusu", "soru", "cevap"]

MIN_KARAKTER_ESIGI = 10
DEGISMEYEN_ORNEK   = 10
SUPHELI_ORNEK      = 20

# ============================================================
#  KONTROL FONKSİYONLARI
# ============================================================

def sutun_kayma_kontrol(df_ori, df_tem):
    print(f"\n{'─'*65}")
    print(f"[1] SÜTUN KAYMASI / BOZULMA KONTROLÜ")
    print(f"{'─'*65}")

    if len(df_ori) != len(df_tem):
        print(f"  ❌ SATIR SAYISI FARKLI! Orijinal: {len(df_ori)}  Temiz: {len(df_tem)}")
    else:
        print(f"  ✅ Satır sayısı eşleşiyor: {len(df_ori)}")

    if list(df_ori.columns) != list(df_tem.columns):
        print(f"  ❌ SÜTUN ADLARI FARKLI!")
        print(f"     Orijinal : {list(df_ori.columns)}")
        print(f"     Temiz    : {list(df_tem.columns)}")
    else:
        print(f"  ✅ Sütun adları eşleşiyor: {list(df_ori.columns)}")

    for sutun in DOKUNULMAYAN_SUTUNLAR:
        if sutun not in df_ori.columns:
            continue
        eslesmeyen = (df_ori[sutun] != df_tem[sutun]).sum()
        if eslesmeyen > 0:
            print(f"  ❌ '{sutun}' sütununda {eslesmeyen} satır farklı — KAYMA VAR!")
        else:
            print(f"  ✅ '{sutun}' sütunu birebir aynı — kayma yok")


def degismeyen_satir_kontrol(df_ori, df_tem):
    print(f"\n{'─'*65}")
    print(f"[2] HİÇ DEĞİŞMEYEN SATIRLAR")
    print(f"{'─'*65}")

    for sutun in TEMIZLENEN_SUTUNLAR:
        if sutun not in df_ori.columns:
            continue
        mask = df_ori[sutun].notna() & (df_ori[sutun] == df_tem[sutun])
        sayi = mask.sum()
        print(f"\n  [{sutun}] Değişmeyen: {sayi} / {len(df_ori)} satır")
        if sayi > 0:
            for i, metin in enumerate(df_ori[mask][sutun].head(DEGISMEYEN_ORNEK), 1):
                print(f"    {i}. {str(metin)[:120]}")


def supheli_satir_kontrol(df_ori, df_tem):
    print(f"\n{'─'*65}")
    print(f"[3] ŞÜPHELİ DEĞİŞİMLER")
    print(f"{'─'*65}")

    for sutun in TEMIZLENEN_SUTUNLAR:
        if sutun not in df_tem.columns:
            continue
        supheli = []
        for i in range(len(df_tem)):
            ori = str(df_ori[sutun].iloc[i]) if pd.notna(df_ori[sutun].iloc[i]) else ""
            tem = str(df_tem[sutun].iloc[i]) if pd.notna(df_tem[sutun].iloc[i]) else ""
            if ori and not tem.strip():
                supheli.append((i, "BOŞ KALDI", ori, tem))
            elif len(ori) > 30 and len(tem) < MIN_KARAKTER_ESIGI:
                supheli.append((i, "ÇOK KISA KALDI", ori, tem))
            elif len(ori) > 50 and len(tem) < len(ori) * 0.2:
                supheli.append((i, f"AŞIRI KISALDI ({len(ori)}→{len(tem)} karakter)", ori, tem))

        print(f"\n  [{sutun}] Şüpheli: {len(supheli)} satır")
        for idx, tip, ori, tem in supheli[:SUPHELI_ORNEK]:
            print(f"\n    Satır {idx+1} — {tip}")
            print(f"    ÖNCE : {ori[:150]}")
            print(f"    SONRA: {tem[:150]}")


def genel_istatistik(df_ori, df_tem):
    print(f"\n{'─'*65}")
    print(f"[4] GENEL İSTATİSTİK")
    print(f"{'─'*65}")

    for sutun in TEMIZLENEN_SUTUNLAR:
        if sutun not in df_ori.columns:
            continue
        ori_len  = df_ori[sutun].dropna().astype(str).str.len()
        tem_len  = df_tem[sutun].dropna().astype(str).str.len()
        degisen  = (df_ori[sutun] != df_tem[sutun]).sum()
        print(f"\n  [{sutun}]")
        print(f"    Değişen satır    : {degisen} / {len(df_ori)}")
        print(f"    Ort. karakter    : {ori_len.mean():.1f} → {tem_len.mean():.1f}")
        print(f"    Toplam karakter  : {ori_len.sum()} → {tem_len.sum()} ({tem_len.sum()-ori_len.sum():+} fark)")


# ============================================================
#  ÇALIŞTIR
# ============================================================

if __name__ == "__main__":
    if not os.path.exists(ORIJINAL):
        print(f"⚠️  Orijinal bulunamadı: {ORIJINAL}"); exit()
    if not os.path.exists(TEMIZ):
        print(f"⚠️  Temiz bulunamadı: {TEMIZ}"); exit()

    df_ori = pd.read_excel(ORIJINAL)
    df_tem = pd.read_excel(TEMIZ)

    print(f"\n{'='*65}")
    print(f"KONTROL: {os.path.basename(TEMIZ)}")
    print(f"{'='*65}")

    sutun_kayma_kontrol(df_ori, df_tem)
    degismeyen_satir_kontrol(df_ori, df_tem)
    supheli_satir_kontrol(df_ori, df_tem)
    genel_istatistik(df_ori, df_tem)

    print(f"\n{'='*65}")
    print("✅ Kontrol tamamlandı.")
    print(f"{'='*65}")