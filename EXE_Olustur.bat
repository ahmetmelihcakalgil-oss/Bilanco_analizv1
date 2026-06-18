@echo off
chcp 65001 >nul
cls
echo ============================================
echo   BIST Analiz EXE Oluşturucu v3.0
echo ============================================
echo.

REM --- Dosya kontrolü ---
echo 📁 Dosyalar kontrol ediliyor...

if not exist "bilanco_analiz_botu_FINAL.py" (
    echo ❌  HATA: bilanco_analiz_botu_FINAL.py bulunamadı!
    echo     Bu dosya aynı klasörde olmalı.
    echo.
    pause
    exit /b 1
)

if not exist "GUI_Arayuz.py" (
    echo ❌  HATA: GUI_Arayuz.py bulunamadı!
    echo.
    pause
    exit /b 1
)

echo ✅  Tüm dosyalar mevcut.
echo.

REM --- PyInstaller kontrolü ---
echo 📦 PyInstaller kontrol ediliyor...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PyInstaller yüklü değil → yükleniyor...
    pip install pyinstaller
    echo ✅  PyInstaller yüklendi.
) else (
    echo ✅  PyInstaller zaten yüklü.
)
echo.

REM --- Gerekli kütüphaneler ---
echo 📦 Gerekli kütüphaneler kontrol ediliyor...
pip install yfinance pandas numpy matplotlib openpyxl --quiet
echo ✅  Kütüphaneler hazır.
echo.

REM --- EXE oluştur ---
echo ============================================
echo 🔨 EXE dosyası oluşturuluyor...
echo    (Bu işlem 1-3 dakika sürebilir)
echo ============================================
echo.

pyinstaller --onefile --windowed --name="BIST_Analiz" --add-data="bilanco_analiz_botu_FINAL.py;." GUI_Arayuz.py

echo.

REM --- Sonuç ---
if exist "dist\BIST_Analiz.exe" (
    echo ============================================
    echo ✅  BAŞARILI! EXE oluşturuldu!
    echo ============================================
    echo.
    echo 📁 Dosya yolu:
    echo    %CD%\dist\BIST_Analiz.exe
    echo.
    echo 💡 ÖNEMLİ:
    echo    EXE çalıştırırken bilanco_analiz_botu_FINAL.py
    echo    dosyasını da AYNI klasöre kopyalayın!
    echo.
    echo    Yani dist\ klasöründe şunlar olmalı:
    echo    ├── BIST_Analiz.exe
    echo    └── bilanco_analiz_botu_FINAL.py
    echo.

    REM dist klasörüne bot dosyasını kopyala
    copy "bilanco_analiz_botu_FINAL.py" "dist\" >nul 2>&1
    echo ✅  Bot dosyası dist\ klasörüne otomatik kopyalandı!
    echo.

    REM dist klasörünü aç
    start "" "dist"
) else (
    echo ============================================
    echo ❌  HATA: EXE oluşturulamadı!
    echo ============================================
    echo.
    echo Yukarıdaki hata mesajlarını kontrol edin.
    echo.
)

pause