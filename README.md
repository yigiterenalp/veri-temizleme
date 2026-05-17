# 🧹 RAG Veri Temizleme ve Hazırlık Hattı (Data Cleaning Pipeline)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-yellow.svg)](https://pandas.pydata.org/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

Bu proje, Büyük Dil Modelleri (LLM) ve **RAG (Retrieval-Augmented Generation)** sistemleri için hazırlanan soru-cevap (QA) veri setlerindeki istenmeyen gürültüleri otomatik olarak temizlemek, analiz etmek ve doğrulamak amacıyla geliştirilmiş kapsamlı bir veri işleme hattıdır.

Özellikle endüstriyel makine model kodları (örn. `BMSO`, `CDGH`), gereksiz takılar (örn. *"makinelerinde"*, *"modelinde"*) ve format hataları özel Regex kalıpları ile temizlenerek yapay zeka modeline en saf bilgi sunulur.

---

## 🚀 Proje İş Akışı (Pipeline)

Süreç birbirini modüler olarak takip eden 5 ana betikten (script) oluşmaktadır:

### 1. 📊 Veri Analizi (`veri_analiz.py`)
Ham Excel veri setinin detaylı bir röntgenini çeker. Sayfa sayısını, boş veri oranlarını, sütun veri tiplerini analiz eder. Metin sütunları için maksimum/minimum karakter istatistiklerini ve yaygın başlangıç kelimelerini tespit eder.

### 2. ✂️ Veri Bölme (`dosya_bol.py`)
Çok büyük veri setlerini belleği yormamak ve paralel işlem yapabilmek adına mantıksal parçalara (örneğin ortadan ikiye) böler ve `bolunmus/` klasörüne kaydeder.

### 3. 🧼 Temizleme Motoru (`rag_temizleyici.py` & `test_temizleyici.py`)
Projenin kalbini oluşturan bu motor, `soru` ve `cevap` sütunları üzerinde çalışır.
- Karmaşık Regex kuralları ile model kodlarını ve cümleye değer katmayan gereksiz ekleri tespit eder.
- Temizleme işlemine başlamadan önce **Önizleme (Preview)** sunarak yapılacak değişiklikleri güvenli bir şekilde gösterir.
- İşlenen veriyi `temizlenmis/` klasörüne kaydeder.

### 4. ✅ Doğrulama ve Güvenlik (`kontrol.py` & `kontrol_test.py`)
Makine öğrenmesi verilerinde veri kaybı yaşanmaması kritiktir. Bu script:
- Orijinal veri ile temizlenmiş veriyi satır satır karşılaştırır.
- Sütun veya satır kaymalarını denetler.
- Aşırı kısalan veya tamamen boş kalan **"şüpheli satırları"** bularak raporlar.

### 5. 🔗 Birleştirme (`birlestir.py`)
Tüm doğrulama aşamalarından başarıyla geçen temizlenmiş veri parçalarını, sütun ve satır bütünlüğünü son kez kontrol ederek nihai bir Excel dosyası haline getirir.

---

## 🛠️ Kullanılan Teknolojiler

* **Python 3**
* **Pandas:** Excel (.xlsx) veri okuma, DataFrame manipülasyonu ve kaydetme işlemleri.
* **Regex (Re):** Gelişmiş dil bilgisi kuralları ve dinamik metin yakalama algoritmaları.
* **OS:** Dosya ve klasör dizini yönetimi.

---

## 📁 Dizin Yapısı

```text
veri-temizleme/
│
├── veri_analiz.py         # Veri istatistikleri ve analiz
├── dosya_bol.py           # Büyük dosyaları parçalara ayırma
├── rag_temizleyici.py     # Eğitim veri seti temizlik algoritması
├── test_temizleyici.py    # Test veri seti temizlik algoritması
├── kontrol.py             # Eğitim seti için satır/sütun kayma kontrolü
├── kontrol_test.py        # Test seti için doğrulama
├── birlestir.py           # Parçaları güvenle birleştirme
│
├── bolunmus/              # (Git'ten hariç tutuldu) Bölünmüş ham veriler
└── temizlenmis/           # (Git'ten hariç tutuldu) Temizlenmiş çıktılar
```
*(Not: Gizlilik ve boyut kısıtlamaları nedeniyle veri setleri (.xlsx dosyaları) Github deposuna dahil edilmemiştir.)*

---

## 💻 Kullanım / Nasıl Çalıştırılır?

Bu projeyi kendi ortamınızda çalıştırmak için:

1. Projeyi bilgisayarınıza indirin (Klonlayın).
2. Gerekli kütüphaneyi kurun:
   ```bash
   pip install pandas openpyxl
   ```
3. İlgili Python dosyalarındaki `AYARLAR` bloğunda yer alan dosya yollarını (path) kendi sisteminize göre güncelleyin.
4. Terminal üzerinden sırasıyla dosyaları çalıştırın:
   ```bash
   python veri_analiz.py
   python dosya_bol.py
   python rag_temizleyici.py
   # ... diğer aşamalar
   ```

---
👨‍💻 **Geliştirici Notu:** Bu proje, İletişim Yazılım Staj programı kapsamında oluşturulmuş olup, uçtan uca modern mimari prensipleriyle geliştirilmiştir.

*Geliştirici:* **Yiğit Eren ALP**  
*Tarih:* 2026
