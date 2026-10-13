# 📊 BIST100 Bilanço Analiz Botu

Borsa İstanbul (BIST) hisselerinin **gerçek finansal verilerini** [Yahoo Finance](https://finance.yahoo.com/) üzerinden çekip **bilanço oran analizi**, **teknik analiz** ve **performans özeti** üreten bir analiz aracıdır. Sonuçları **grafik (PNG)** ve **Excel raporu** olarak kaydeder.

Proje üç farklı arayüzle kullanılabilir:

- 🖥️ **Komut Satırı (CLI)** — hızlı terminal kullanımı
- 🪟 **Masaüstü GUI (Tkinter)** — kod bilgisi gerektirmeyen pencere arayüzü
- 🌐 **Web Arayüzü (Streamlit)** — tarayıcıda çalışan, SWOT/yönetici özeti ve 0–100 skorlama içeren arayüz

---

## ✨ Özellikler

- 📥 Yahoo Finance (`yfinance`) ile **gerçek** BIST verisi (`.IS` uzantısı)
- 📈 Finansal oran analizi (karlılık, likidite, borçlanma, piyasa)
- 📉 Teknik analiz (MA20 / MA50 ve trend sinyali)
- 🕯️ 4 panelli otomatik grafik: fiyat + hareketli ortalamalar, hacim, mum grafiği, getiri dağılımı
- 📑 Çok sayfalı Excel raporu (Karlılık, Likidite, Borçlanma, Piyasa, Fiyat Tarihi)
- 🧮 Web arayüzünde **0–100 genel değerlendirme skoru** + güçlü/zayıf yön analizi
- 📦 PyInstaller ile tek dosyalık `BIST_Analiz.exe` üretimi

### Hesaplanan Oranlar

| Kategori | Göstergeler |
|---|---|
| 💰 Karlılık | ROE, ROA, Net Kar Marjı, F/K Oranı |
| 💧 Likidite | Cari Oran, Asit Test Oranı |
| 📉 Borçlanma | Borç/Özkaynak, Toplam Borç/Toplam Varlık |
| 📈 Piyasa | Güncel Fiyat, Günlük Değişim, Piyasa Değeri, PD/DD |

---

## 🗂️ Proje Yapısı

```
Bilanco_analizv1/
├── bilanco_analiz_botu_FINAL.py   → çekirdek: veri çekme + analiz + grafik + Excel
├── GUI_Arayuz.py                  → masaüstü (Tkinter) arayüz
├── Web_Arayuz.py                  → web (Streamlit) arayüz
├── BIST_Analiz.spec               → PyInstaller derleme tanımı
├── EXE_Olustur.bat                → Windows'ta tek tıkla .exe üretme betiği
├── dist/BIST_Analiz.exe           → derlenmiş çalıştırılabilir dosya
├── ASELS_analiz_grafigi.png       → örnek çıktılar
├── THYAO_analiz_raporu.xlsx
└── README.md
```

---

## 🚀 Kurulum

Depoyu klonlayıp gerekli kütüphaneleri kurun:

```bash
git clone https://github.com/ahmetmelihcakalgil-oss/Bilanco_analizv1
cd Bilanco_analizv1

pip install yfinance pandas numpy matplotlib openpyxl streamlit
```

---

## ▶️ Çalıştırma

**1) Komut satırı (CLI):**

```bash
python bilanco_analiz_botu_FINAL.py
# Menüden "1" seçip hisse kodunu girin (ör. ASELS, THYAO, GARAN)
```

**2) Masaüstü arayüz (Tkinter):**

```bash
python GUI_Arayuz.py
```

**3) Web arayüzü (Streamlit):**

```bash
streamlit run Web_Arayuz.py
```

**4) Çalıştırılabilir dosya (.exe):**

`dist/BIST_Analiz.exe` dosyasını çift tıklayarak çalıştırabilirsiniz. Kendiniz derlemek için:

```bash
EXE_Olustur.bat
```

---

## 📤 Çıktılar

Uygulama çalıştığı klasöre şu dosyaları üretir:

- `<SEMBOL>_analiz_grafigi.png` — 4 panelli analiz grafiği
- `<SEMBOL>_analiz_raporu.xlsx` — çok sayfalı finansal rapor

Web arayüzünde ayrıca ekrandan indirme butonları ve yönetici özeti (SWOT) sunulur.

---

## ⚠️ Bilinen Sınırlamalar

- **Veri kaynağı:** Analizler Yahoo Finance'e dayanır; bazı BIST hisselerinde veri eksik veya gecikmeli olabilir. Yatırım tavsiyesi değildir.
- **BİST100 listesi** kod içinde sabit tanımlıdır (`bist100_listesi()`), güncel endeks bileşenlerini içermeyebilir.
- `build/` ve `dist/` klasörleri (derleme çıktıları, ~90 MB) depoya dahil edilmiştir; veri/derleme dosyalarının `.gitignore` ile hariç tutulması önerilir.
- Arayüzler yalnızca BIST (`.IS`) sembollerine göre çalışır.

---

## 🛠️ Teknolojiler

`Python` · `yfinance` · `pandas` · `numpy` · `matplotlib` · `openpyxl` · `Tkinter` · `Streamlit` · `PyInstaller`

---

## 📄 Lisans

MIT

> ⚠️ Bu araç yalnızca eğitim/araştırma amaçlıdır ve **yatırım tavsiyesi değildir**.
