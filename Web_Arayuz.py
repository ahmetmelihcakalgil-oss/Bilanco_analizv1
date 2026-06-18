#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIST Bilanço Analiz - Web Arayüzü (Streamlit)
Tarayıcıda çalışır - Kod bilgisi gerektirmez!

Kurulum: pip install streamlit
Çalıştır: streamlit run Web_Arayuz.py
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="BIST Bilanço Analiz",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { padding: 1.5rem; }
    .stButton>button {
        width: 100%;
        background-color: #2E86DE !important;
        color: white !important;
        font-size: 17px !important;
        padding: 0.7rem !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
    }
    .stButton>button:hover {
        background-color: #1e5fc4 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Bot import
try:
    from bilanco_analiz_botu_FINAL import BilancoAnalizBotu, bist100_listesi
    BOT_MEVCUT = True
except Exception as e:
    BOT_MEVCUT = False
    IMPORT_HATA = str(e)


def safe_float(value, default=0.0):
    """Değeri güvenli şekilde float'a çevir"""
    try:
        v = float(value)
        return v if v == v else default  # NaN kontrolü
    except (TypeError, ValueError):
        return default


def main():
    # --- Başlık ---
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("📊 BIST100 Bilanço Analiz Botu")
        st.markdown("Profesyonel finansal analiz")
    with col2:
        st.metric("Versiyon", "v3.0")

    st.divider()

    # --- Sidebar ---
    with st.sidebar:
        st.header("⚙️ Ayarlar")

        st.subheader("🏢 Şirket Seçimi")

        populer = [
            "Kendin Gir",
            "ASELS – ASELSAN",
            "THYAO – Türk Hava Yolları",
            "GARAN – Garanti Bankası",
            "AKBNK – Akbank",
            "YKBNK – Yapi Kredi",
            "EREGL – Ereğli Demir",
            "TUPRS – Tüpraş",
            "KCHOL – Koç Holding",
            "BIMAS – BİM",
            "TTKOM – Türk Telekom"
        ]

        secim = st.selectbox("Popüler Şirketler:", populer)

        if secim == "Kendin Gir":
            sembol = st.text_input("Hisse Kodu Yazın:", "ASELS", max_chars=10).strip().upper()
        else:
            sembol = secim.split(" ")[0]

        st.divider()

        st.subheader("📋 Analiz Seçenekleri")
        grafik = st.checkbox("📊 Grafik Oluştur", value=True)
        excel  = st.checkbox("📑 Excel Raporu",   value=True)
        detay  = st.checkbox("📝 Detaylı Oranlar", value=True)

        st.divider()

        st.info("""
        💡 **Nasıl Kullanılır?**
        1. Hisse kodu seçin veya yazın
        2. İstediğiniz seçenekleri işaretleyin
        3. 'Analizi Başlat' butonuna tıklayın
        """)

    # --- Bot kontrolü ---
    if not BOT_MEVCUT:
        st.error(f"❌ Bot dosyası bulunamadı!\n\n`bilanco_analiz_botu_FINAL.py` dosyasını bu programla aynı klasöre koyun.\n\nHata: {IMPORT_HATA}")
        return

    st.subheader(f"🎯 Seçili Hisse: {sembol}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Hisse Kodu", sembol)
    col2.metric("Kaynak", "Yahoo Finance")
    col3.metric("Durum", "Hazır ✅")

    st.divider()

    if st.button("🚀 Analizi Başlat"):
        analiz_yap(sembol, grafik, excel, detay)


def analiz_yap(sembol, grafik, excel, detay):
    progress = st.progress(0, text="Başlatılıyor...")

    try:
        progress.progress(15, text="📊 Bot başlatılıyor...")
        bot = BilancoAnalizBotu(sirket_kodu=sembol)

        progress.progress(30, text="📥 Yahoo Finance'den veri çekiliyor...")
        bot.tum_analizleri_yap()

        progress.progress(55, text="🔍 Oranlar hesaplandı!")

        st.success(f"✅ {sembol} verileri başarıyla alındı!")

        # --- Oranları güvenli şekilde çek ---
        roe     = safe_float(bot.oranlar['karlilik'].get('ROE (%)',         0))
        nkm     = safe_float(bot.oranlar['karlilik'].get('Net Kar Marjı (%)', 0))
        fk      = safe_float(bot.oranlar['karlilik'].get('F/K Oranı',       0))
        cari    = safe_float(bot.oranlar['likidite'].get('Cari Oran',        0))
        asit    = safe_float(bot.oranlar['likidite'].get('Asit Test Oranı',  0))
        borc_oz = safe_float(bot.oranlar['borclanma'].get('Borç/Özkaynak (%)', 0))
        borc_va = safe_float(bot.oranlar['borclanma'].get('Toplam Borç/Toplam Varlık (%)', 0))
        fiyat   = safe_float(bot.oranlar['piyasa'].get('Güncel Fiyat (TL)', 0))
        degisim = safe_float(bot.oranlar['piyasa'].get('Günlük Değişim (%)', 0))
        pddd    = safe_float(bot.oranlar['piyasa'].get('PD/DD Oranı',        0))

        # --- Özet kartlar ---
        st.subheader("📊 Finansal Özet")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💰 Fiyat (TL)",    f"{fiyat:.2f}",   delta=f"{degisim:+.2f}%")
        c2.metric("📈 ROE ❓",         f"{roe:.2f}%",
                  help="Return on Equity (Özkaynak Karlılığı): Şirketin öz sermayesiyle ne kadar kâr ettiğini gösterir. Yüksek ROE, yönetimin parayı verimli kullandığı anlamına gelir. Genel kural: %15 üzeri iyi, %20 üzeri mükemmel.")
        c3.metric("💧 Cari Oran",     f"{cari:.2f}",
                  help="Şirketin kısa vadeli borçlarını ödeme gücünü gösterir. 1.0'ın altı risk sinyali, 1.5–2.0 arası sağlıklı kabul edilir.")
        c4.metric("📉 Borç/Özkaynak", f"{borc_oz:.0f}%",
                  help="Şirketin ne kadar borçla çalıştığını gösterir. Düşük olması finansal riski azaltır.")

        # --- Detaylı oranlar ---
        if detay:
            progress.progress(65, text="📋 Detaylı tablolar hazırlanıyor...")
            st.subheader("📋 Detaylı Finansal Oranlar")

            ACIKLAMALAR = {
                'ROE (%)':              'Return on Equity — Özkaynak karlılığı. Şirketin öz sermayesiyle ne kadar kâr ettiğini gösterir. %15+ iyi, %20+ mükemmel.',
                'ROA (%)':              'Return on Assets — Varlık karlılığı. Şirketin toplam varlıklarını ne kadar verimli kullandığını gösterir. %5+ iyi, %10+ güçlü.',
                'Net Kar Marjı (%)':    'Her 100 TL gelirden kalan net kâr. Yüksek olması şirketin maliyet kontrolünün güçlü olduğunu gösterir.',
                'F/K Oranı':            'Fiyat/Kazanç oranı. Hissenin kazancına göre kaç katına işlem gördüğünü gösterir. Düşük F/K ucuz, yüksek F/K pahalı sinyali verebilir.',
                'Cari Oran':            'Dönen varlıklar / Kısa vadeli borçlar. 1.0 altı risk, 1.5–2.0 arası sağlıklı.',
                'Asit Test Oranı':      'Stoklar hariç likidite ölçüsü. Cari orandan daha katı bir testtir. 1.0 üzeri iyi.',
                'Borç/Özkaynak (%)':    'Toplam borç / Özkaynak. Şirketin finansman yapısını gösterir. Düşük olması daha az finansal risk demektir.',
                'Toplam Borç/Toplam Varlık (%)': 'Varlıkların ne kadarının borçla finanse edildiğini gösterir. %50 altı tercih edilir.',
                'Güncel Fiyat (TL)':    'Son kapanış fiyatı.',
                'Günlük Değişim (%)':   'Bir önceki kapanışa göre yüzde değişim.',
                'Piyasa Değeri (TL)':   'Toplam hisse sayısı × güncel fiyat.',
                'PD/DD Oranı':          'Piyasa Değeri / Defter Değeri. 1.0 altı teorik olarak ucuz, çok yüksek ise pahalı olabilir.',
            }

            def df_aciklamali(oranlar_dict):
                rows = []
                for k, v in oranlar_dict.items():
                    rows.append({'Gösterge': k, 'Değer': v, 'Açıklama': ACIKLAMALAR.get(k, '—')})
                return pd.DataFrame(rows)

            tab1, tab2, tab3, tab4 = st.tabs(["💰 Karlılık", "💧 Likidite", "📉 Borçlanma", "📈 Piyasa"])

            with tab1:
                st.dataframe(df_aciklamali(bot.oranlar['karlilik']), use_container_width=True, hide_index=True)
            with tab2:
                st.dataframe(df_aciklamali(bot.oranlar['likidite']), use_container_width=True, hide_index=True)
            with tab3:
                st.dataframe(df_aciklamali(bot.oranlar['borclanma']), use_container_width=True, hide_index=True)
            with tab4:
                st.dataframe(df_aciklamali(bot.oranlar['piyasa']), use_container_width=True, hide_index=True)

        # --- Dosya üretim ---
        dosyalar = []

        if grafik:
            progress.progress(75, text="📊 Grafik oluşturuluyor...")
            g = bot.trend_analizi_grafik()
            dosyalar.append(("Grafik (PNG)", g))

        if excel:
            progress.progress(85, text="📑 Excel hazırlanıyor...")
            x = bot.karsilastirma_excel()
            dosyalar.append(("Excel Rapor", x))

        progress.progress(95, text="🏁 Son adımlar...")

        # --- İndirme ---
        if dosyalar:
            st.subheader("📥 Dosya İndirme")
            cols = st.columns(len(dosyalar))
            for col, (tip, yol) in zip(cols, dosyalar):
                if os.path.exists(yol):
                    with open(yol, 'rb') as f:
                        col.download_button(
                            label=f"⬇️ {tip} İndir",
                            data=f,
                            file_name=os.path.basename(yol),
                            mime='application/octet-stream',
                            use_container_width=True
                        )

        # ─────────────────────────────────────────────────────────────
        # SWOT / Yönetici Özeti  (DÜZELTİLDİ)
        # ─────────────────────────────────────────────────────────────
        st.subheader("📌 Yönetici Özeti")

        col_g, col_w = st.columns(2)

        with col_g:
            st.markdown("### ✅ Güçlü Yönler")
            guc = []

            if roe >= 15:
                guc.append(f"Yüksek özkaynak karlılığı (ROE: {roe:.1f}%)")
            elif roe >= 10:
                guc.append(f"Orta düzey karlılık (ROE: {roe:.1f}%)")

            if nkm >= 10:
                guc.append(f"Güçlü net kar marjı ({nkm:.1f}%)")
            elif nkm > 0:
                guc.append(f"Pozitif net kar marjı ({nkm:.1f}%)")

            if cari >= 1.5:
                guc.append(f"Sağlam likidite (Cari Oran: {cari:.2f})")
            elif cari >= 1.0:
                guc.append(f"Yeterli likidite (Cari Oran: {cari:.2f})")

            if borc_oz <= 100:
                guc.append(f"Dengeli borçluluk (B/Ö: {borc_oz:.0f}%)")

            if fk > 0 and fk <= 10:
                guc.append(f"Ucuz fiyatlama (F/K: {fk:.1f}x)")

            if not guc:
                guc.append("Veri yetersiz veya analiz için eşik değerler karşılanamadı")

            for madde in guc:
                st.markdown(f"• {madde}")

        with col_w:
            st.markdown("### ⚠️ Dikkat Edilmesi Gerekenler")
            dikkat = []

            if roe < 10:
                dikkat.append(f"Karlılık artırılmalı (ROE: {roe:.1f}%)")

            if nkm <= 0:
                dikkat.append("Net zarar durumu mevcut")
            elif nkm < 5:
                dikkat.append(f"Düşük kar marjı ({nkm:.1f}%)")

            if cari < 1.0:
                dikkat.append(f"Likidite riski (Cari Oran: {cari:.2f})")
            elif cari < 1.5:
                dikkat.append(f"Cari oran iyileştirilebilir ({cari:.2f})")

            if borc_oz > 200:
                dikkat.append(f"Çok yüksek borç yükü (B/Ö: {borc_oz:.0f}%)")
            elif borc_oz > 100:
                dikkat.append(f"Yüksek borçluluk (B/Ö: {borc_oz:.0f}%)")

            if fk > 20:
                dikkat.append(f"Pahalı fiyatlama (F/K: {fk:.1f}x)")

            if not dikkat:
                dikkat.append("Genel tablo olumlu görünüyor")

            for madde in dikkat:
                st.markdown(f"• {madde}")

        # ─────────────────────────────────────────────────────────────
        # SKOR HESAPLAMA  (DÜZELTİLDİ)
        # ─────────────────────────────────────────────────────────────
        st.subheader("📊 Genel Değerlendirme")

        skor = 0
        skor_detay = []

        # Karlılık (toplam 35 puan)
        if roe >= 20:
            skor += 20; skor_detay.append("ROE ≥ 20% → +20")
        elif roe >= 15:
            skor += 15; skor_detay.append("ROE ≥ 15% → +15")
        elif roe >= 10:
            skor += 10; skor_detay.append("ROE ≥ 10% → +10")
        elif roe > 0:
            skor += 5;  skor_detay.append("ROE > 0% → +5")

        if nkm >= 15:
            skor += 15; skor_detay.append("Net Kar Marjı ≥ 15% → +15")
        elif nkm >= 10:
            skor += 10; skor_detay.append("Net Kar Marjı ≥ 10% → +10")
        elif nkm >= 5:
            skor += 7;  skor_detay.append("Net Kar Marjı ≥ 5% → +7")
        elif nkm > 0:
            skor += 3;  skor_detay.append("Net Kar Marjı > 0% → +3")

        # Likidite (toplam 25 puan)
        if cari >= 2.0:
            skor += 25; skor_detay.append("Cari Oran ≥ 2.0 → +25")
        elif cari >= 1.5:
            skor += 20; skor_detay.append("Cari Oran ≥ 1.5 → +20")
        elif cari >= 1.0:
            skor += 12; skor_detay.append("Cari Oran ≥ 1.0 → +12")
        elif cari > 0:
            skor += 5;  skor_detay.append("Cari Oran > 0 → +5")

        # Borçlanma (toplam 25 puan)
        if borc_oz <= 50:
            skor += 25; skor_detay.append("Borç/Özkaynak ≤ 50% → +25")
        elif borc_oz <= 100:
            skor += 20; skor_detay.append("Borç/Özkaynak ≤ 100% → +20")
        elif borc_oz <= 150:
            skor += 12; skor_detay.append("Borç/Özkaynak ≤ 150% → +12")
        elif borc_oz <= 200:
            skor += 5;  skor_detay.append("Borç/Özkaynak ≤ 200% → +5")

        # Piyasa değerlemesi (toplam 15 puan)
        if 0 < fk <= 10:
            skor += 15; skor_detay.append("F/K ≤ 10 → +15")
        elif 0 < fk <= 15:
            skor += 10; skor_detay.append("F/K ≤ 15 → +10")
        elif 0 < fk <= 25:
            skor += 5;  skor_detay.append("F/K ≤ 25 → +5")

        skor = min(skor, 100)

        # Skor göster
        st.progress(skor / 100)
        st.write(f"**Toplam Skor: {skor}/100**")

        # Detay expander
        with st.expander("Skor detayını göster"):
            if skor_detay:
                for d in skor_detay:
                    st.write(f"  ✔ {d}")
            else:
                st.write("Hiçbir eşik değer karşılanamadı — veri eksik olabilir.")

            # Eksik / sıfır gelen verileri göster
            eksik = []
            if nkm == 0:  eksik.append(f"Net Kar Marjı: 0 veya veri yok → puan eklenmedi")
            if borc_oz == 0: eksik.append(f"Borç/Özkaynak: 0 veya veri yok → puan eklenmedi")
            if fk == 0:   eksik.append(f"F/K Oranı: 0 veya veri yok → puan eklenmedi")
            if cari == 0: eksik.append(f"Cari Oran: 0 veya veri yok → puan eklenmedi")
            if roe == 0:  eksik.append(f"ROE: 0 veya veri yok → puan eklenmedi")
            if eksik:
                st.markdown("---")
                st.markdown("**⚠️ Veri gelmeyenler (Yahoo Finance'de mevcut değil):**")
                for e in eksik:
                    st.write(f"  ✖ {e}")

        # Değerlendirme etiketi
        if skor >= 80:
            st.success("⭐⭐⭐⭐⭐ MÜKEMMEL — Çok güçlü finansal durum")
        elif skor >= 65:
            st.success("⭐⭐⭐⭐ ÇOK İYİ — Sağlam finansal yapı")
        elif skor >= 50:
            st.info("⭐⭐⭐ İYİ — Orta seviye finansal sağlık")
        elif skor >= 30:
            st.warning("⭐⭐ ORTA — İyileştirme gerekli")
        else:
            st.error("⭐ ZAYIF — Veri eksik veya finansal yapı zorlu")

        progress.progress(100, text="✅ Tamamlandı!")

    except Exception as e:
        st.error(f"❌ Hata oluştu: {e}")
        import traceback
        st.code(traceback.format_exc())


if __name__ == "__main__":
    main()