#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIST100 Bilanço Analiz Botu v3.0 - YAHOO FINANCE
GERÇEK VERİ - Tüm BIST hisseleri için çalışır
Kurulum: pip install yfinance
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'DejaVu Sans'

class YahooFinanceVeri:
    """Yahoo Finance'den GERÇEK BIST verisi çeker"""
    
    def __init__(self):
        self.suffix = ".IS"  # Istanbul Stock Exchange
    
    def hisse_getir(self, sembol):
        """Hisse verisini çek"""
        ticker_symbol = f"{sembol}{self.suffix}"
        
        try:
            print(f"🔍 {sembol} için Yahoo Finance'den GERÇEK veri çekiliyor...")
            ticker = yf.Ticker(ticker_symbol)
            
            info = ticker.info
            hist = ticker.history(period="1y")
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cashflow = ticker.cashflow
            
            if not hist.empty:
                print(f"✅ {sembol} - GERÇEK VERİ ALINDI!")
                print(f"   • Güncel fiyat: {hist['Close'].iloc[-1]:.2f} TL")
                print(f"   • Piyasa değeri: {info.get('marketCap', 'N/A')}")
                print(f"   • Sektör: {info.get('sector', 'N/A')}")
                
                return {
                    'ticker': ticker,
                    'info': info,
                    'history': hist,
                    'financials': financials,
                    'balance_sheet': balance_sheet,
                    'cashflow': cashflow
                }
            else:
                print(f"⚠️  {sembol} için veri bulunamadı")
                return None
                
        except Exception as e:
            print(f"⚠️  Hata: {str(e)[:100]}")
            return None


class BilancoAnalizBotu:
    """
    GUI ve Web arayüzlerinden çağrılabilir ana analiz klası.
    Yahoo Finance'den gerçek veri çeker ve analiz yapar.
    """
    
    def __init__(self, sirket_kodu="ASELS", calisma_dizini=None):
        self.sembol = sirket_kodu.upper()
        self.veri_api = YahooFinanceVeri()
        self.data = None
        self.oranlar = {
            'karlilik': {},
            'likidite': {},
            'borclanma': {},
            'piyasa': {}
        }
        
        if calisma_dizini is None:
            self.calisma_dizini = os.getcwd()
        else:
            self.calisma_dizini = calisma_dizini
    
    def tum_analizleri_yap(self):
        """Tüm analizleri çalıştır"""
        print(f"\n{'='*70}")
        print(f"🚀 {self.sembol} - GERÇEK VERİ ANALİZİ")
        print(f"{'='*70}\n")
        
        self.data = self.veri_api.hisse_getir(self.sembol)
        
        if not self.data:
            raise Exception(f"{self.sembol} için veri bulunamadı. Hisse kodu doğru mu kontrol edin.")
        
        self._oranlar_hesapla()
        self._temel_bilgiler()
        self._teknik_analiz()
        self._performans_analizi()
        
        return True
    
    def _oranlar_hesapla(self):
        """Finansal oranları hesapla"""
        info = self.data['info']
        hist = self.data['history']
        
        # --- Karlılık ---
        pe = info.get('trailingPE', 0) or 0
        roe = info.get('returnOnEquity', 0) or 0
        roa = info.get('returnOnAssets', 0) or 0
        profit_margin = info.get('profitMargin', 0) or 0
        
        self.oranlar['karlilik'] = {
            'ROE (%)': round(roe * 100, 2),
            'ROA (%)': round(roa * 100, 2),
            'Net Kar Marjı (%)': round(profit_margin * 100, 2),
            'F/K Oranı': round(pe, 2)
        }
        
        # --- Likidite ---
        current_ratio = info.get('currentRatio', 0) or 0
        quick_ratio = info.get('quickRatio', 0) or 0
        
        self.oranlar['likidite'] = {
            'Cari Oran': round(current_ratio, 2),
            'Asit Test Oranı': round(quick_ratio, 2)
        }
        
        # --- Borçlanma ---
        debt_equity = info.get('debtToEquity', 0) or 0
        total_debt = info.get('totalDebt', 0) or 0
        total_assets = info.get('totalAssets', 0) or 1
        
        self.oranlar['borclanma'] = {
            'Borç/Özkaynak (%)': round(debt_equity * 100, 2),
            'Toplam Borç/Toplam Varlık (%)': round((total_debt / total_assets) * 100, 2) if total_assets else 0
        }
        
        # --- Piyasa ---
        market_cap = info.get('marketCap', 0) or 0
        guncel_fiyat = hist['Close'].iloc[-1]
        onceki_kapanis = hist['Close'].iloc[-2]
        degisim = ((guncel_fiyat - onceki_kapanis) / onceki_kapanis) * 100
        
        self.oranlar['piyasa'] = {
            'Güncel Fiyat (TL)': round(guncel_fiyat, 2),
            'Günlük Değişim (%)': round(degisim, 2),
            'Piyasa Değeri (TL)': market_cap,
            'PD/DD Oranı': round(info.get('priceToBook', 0) or 0, 2)
        }
    
    def _temel_bilgiler(self):
        """Temel bilgileri yazdır"""
        info = self.data['info']
        hist = self.data['history']
        
        print("\n📊 TEMEL BİLGİLER")
        print("-"*40)
        print(f"🏢 Şirket : {info.get('longName', self.sembol)}")
        print(f"📍 Sektör : {info.get('sector', 'Bilinmiyor')}")
        print(f"🏭 Endüstri: {info.get('industry', 'Bilinmiyor')}")
        print(f"💰 Fiyat  : {hist['Close'].iloc[-1]:.2f} TL")
        print(f"📈 Değişim: {self.oranlar['piyasa']['Günlük Değişim (%)']:+.2f}%")
    
    def _teknik_analiz(self):
        """Teknik analiz"""
        hist = self.data['history']
        
        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        
        guncel = hist['Close'].iloc[-1]
        ma20 = hist['MA20'].iloc[-1]
        ma50 = hist['MA50'].iloc[-1]
        
        print("\n📈 TEKNİK ANALİZ")
        print("-"*40)
        print(f"   MA20 : {ma20:.2f} TL")
        print(f"   MA50 : {ma50:.2f} TL")
        
        if guncel > ma20 > ma50:
            print("   🎯 Sinyal: ✅ YUKARI TREND")
        elif guncel < ma20 < ma50:
            print("   🎯 Sinyal: ❌ AŞAĞI TREND")
        else:
            print("   🎯 Sinyal: ⚠️  KARARSIZ")
    
    def _performans_analizi(self):
        """Performans metrikleri"""
        hist = self.data['history']
        
        gunluk  = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-2]) - 1) * 100
        haftalik = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-5]) - 1) * 100 if len(hist) >= 5 else 0
        aylik   = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-20]) - 1) * 100 if len(hist) >= 20 else 0
        yillik  = ((hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1) * 100
        
        volatilite = hist['Close'].pct_change().std() * np.sqrt(252) * 100
        
        print("\n📊 PERFORMANS")
        print("-"*40)
        print(f"   Günlük   : {gunluk:+.2f}%")
        print(f"   Haftalık : {haftalik:+.2f}%")
        print(f"   Aylık    : {aylik:+.2f}%")
        print(f"   Yıllık   : {yillik:+.2f}%")
        print(f"   Volatilite: {volatilite:.2f}%")
    
    def trend_analizi_grafik(self):
        """Grafik oluştur ve dosya yolunu döndür"""
        hist = self.data['history']
        
        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle(f'{self.sembol} - Analiz Grafiği', fontsize=16, fontweight='bold')
        
        # 1. Fiyat + MA
        ax1 = axes[0, 0]
        ax1.plot(hist.index, hist['Close'], label='Fiyat', linewidth=2, color='#2E86DE')
        ax1.plot(hist.index, hist['MA20'], label='MA20', linewidth=1.5, color='#10AC84', linestyle='--', alpha=0.7)
        ax1.plot(hist.index, hist['MA50'], label='MA50', linewidth=1.5, color='#EE5A6F', linestyle='--', alpha=0.7)
        ax1.set_title('Fiyat ve Hareketli Ortalamalar', fontweight='bold')
        ax1.set_ylabel('Fiyat (TL)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Hacim
        ax2 = axes[0, 1]
        colors = ['green' if hist['Close'].iloc[i] >= hist['Open'].iloc[i] else 'red' for i in range(len(hist))]
        ax2.bar(hist.index, hist['Volume'], color=colors, alpha=0.6)
        ax2.set_title('İşlem Hacmi', fontweight='bold')
        ax2.set_ylabel('Hacim')
        ax2.grid(True, alpha=0.3)
        
        # 3. Mum grafiği
        ax3 = axes[1, 0]
        for i in range(len(hist)):
            color = 'green' if hist['Close'].iloc[i] >= hist['Open'].iloc[i] else 'red'
            ax3.plot([hist.index[i], hist.index[i]], [hist['Low'].iloc[i], hist['High'].iloc[i]], color=color, linewidth=0.5)
            ax3.plot([hist.index[i], hist.index[i]], [hist['Open'].iloc[i], hist['Close'].iloc[i]], color=color, linewidth=3)
        ax3.set_title('Mum Grafiği', fontweight='bold')
        ax3.set_ylabel('Fiyat (TL)')
        ax3.grid(True, alpha=0.3)
        
        # 4. Getiri dağılımı
        ax4 = axes[1, 1]
        returns = hist['Close'].pct_change() * 100
        ax4.hist(returns.dropna(), bins=50, color='#9C27B0', alpha=0.7, edgecolor='black')
        ax4.axvline(returns.mean(), color='red', linestyle='--', linewidth=2, label=f'Ortalama: {returns.mean():.2f}%')
        ax4.set_title('Günlük Getiri Dağılımı', fontweight='bold')
        ax4.set_xlabel('Getiri (%)')
        ax4.set_ylabel('Frekans')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        grafik_dosya = os.path.join(self.calisma_dizini, f'{self.sembol}_analiz_grafigi.png')
        plt.savefig(grafik_dosya, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✅ Grafik kaydedildi: {grafik_dosya}")
        plt.close()
        
        return grafik_dosya
    
    def karsilastirma_excel(self):
        """Excel raporu oluştur ve dosya yolunu döndür"""
        try:
            excel_dosya = os.path.join(self.calisma_dizini, f'{self.sembol}_analiz_raporu.xlsx')
            
            with pd.ExcelWriter(excel_dosya, engine='openpyxl') as writer:
                # Karlılık
                pd.DataFrame(list(self.oranlar['karlilik'].items()), columns=['Gösterge', 'Değer']).to_excel(
                    writer, sheet_name='Karlılık', index=False)
                
                # Likidite
                pd.DataFrame(list(self.oranlar['likidite'].items()), columns=['Gösterge', 'Değer']).to_excel(
                    writer, sheet_name='Likidite', index=False)
                
                # Borçlanma
                pd.DataFrame(list(self.oranlar['borclanma'].items()), columns=['Gösterge', 'Değer']).to_excel(
                    writer, sheet_name='Borçlanma', index=False)
                
                # Piyasa
                pd.DataFrame(list(self.oranlar['piyasa'].items()), columns=['Gösterge', 'Değer']).to_excel(
                    writer, sheet_name='Piyasa', index=False)
                
                # Fiyat tarihi
                if self.data and not self.data['history'].empty:
                    hist = self.data['history'].copy()
                    hist.index = hist.index.tz_localize(None)  # timezone kaldır
                    hist.to_excel(writer, sheet_name='Fiyat Tarihi')
            
            print(f"✅ Excel raporu kaydedildi: {excel_dosya}")
            return excel_dosya
            
        except Exception as e:
            print(f"⚠️  Excel oluşturma hatası: {e}")
            raise


def bist100_listesi():
    """BIST100 hisselerini listele"""
    return sorted([
        'ASELS', 'THYAO', 'GARAN', 'AKBNK', 'YKBNK', 'ISCTR', 'HALKB',
        'EREGL', 'KCHOL', 'SAHOL', 'TUPRS', 'PETKM', 'SISE', 'ENKAI',
        'ARCLK', 'BIMAS', 'TAVHL', 'KOZAL', 'KOZAA', 'TTKOM', 'TOASO',
        'FROTO', 'VESTL', 'PGSUS', 'SODA', 'EKGYO', 'ODAS', 'MGROS',
        'SOKM', 'ULKER', 'CCOLA', 'AEFES', 'TCELL', 'DOHOL', 'LOGO',
        'SELEC', 'TTRAK', 'GESAN', 'ISGYO', 'AKSUE', 'AGHOL', 'MAVI',
        'OYAKC', 'IZMDC', 'SKBNK', 'VAKBN', 'HEKTS', 'DOAS',
        'BRSAN', 'IPEKE', 'GUBRF', 'ASUZU', 'TSKB', 'ALARK', 'BFREN'
    ])


if __name__ == "__main__":
    # Standalone mod - terminal'den çalışabilir
    print("\n🎯 BIST ANALİZ BOTU v3.0\n")
    
    try:
        import yfinance
    except ImportError:
        print("❌ yfinance yüklü değil! → pip install yfinance")
        exit()
    
    print("1. Tek hisse analizi")
    print("2. BIST100 listesi")
    print("3. Çıkış\n")
    
    secim = input("Seçiminiz: ").strip()
    
    if secim == "1":
        sembol = input("Hisse kodu: ").strip().upper()
        bot = BilancoAnalizBotu(sirket_kodu=sembol)
        bot.tum_analizleri_yap()
        bot.trend_analizi_grafik()
        bot.karsilastirma_excel()
    elif secim == "2":
        for i, s in enumerate(bist100_listesi(), 1):
            print(f"{i:2d}. {s}", end="    ")
            if i % 8 == 0: print()