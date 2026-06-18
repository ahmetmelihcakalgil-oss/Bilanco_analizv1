#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIST Bilanço Analiz - Kullanıcı Dostu GUI Arayüz
Kod bilgisi gerektirmez!
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import sys
from datetime import datetime

# Bot import
try:
    from bilanco_analiz_botu_FINAL import BilancoAnalizBotu, bist100_listesi
    BOT_MEVCUT = True
except Exception as e:
    BOT_MEVCUT = False
    IMPORT_HATA = str(e)


class BilancoAnalizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 BIST100 Bilanço Analiz Botu v3.0")
        self.root.geometry("750x650")
        self.root.resizable(False, False)

        self.bg_color = "#f0f0f0"
        self.accent_color = "#2E86DE"
        self.root.configure(bg=self.bg_color)

        self.create_widgets()

    def create_widgets(self):
        # --- Başlık ---
        baslik_frame = tk.Frame(self.root, bg=self.accent_color, height=75)
        baslik_frame.pack(fill=tk.X)
        baslik_frame.pack_propagate(False)

        tk.Label(
            baslik_frame,
            text="📊  BIST100 Bilanço Analiz Botu  v3.0",
            font=("Arial", 19, "bold"),
            bg=self.accent_color, fg="white"
        ).pack(pady=22)

        # --- Ana frame ---
        main = tk.Frame(self.root, bg=self.bg_color)
        main.pack(fill=tk.BOTH, expand=True, padx=22, pady=18)

        # --- Şirket Seçimi ---
        secim_frame = tk.LabelFrame(main, text="🏢  Şirket Seçimi",
                                    font=("Arial", 11, "bold"), bg=self.bg_color, padx=12, pady=10)
        secim_frame.pack(fill=tk.X, pady=(0, 12))

        tk.Label(secim_frame, text="Hisse Kodu:", font=("Arial", 10), bg=self.bg_color
                 ).grid(row=0, column=0, sticky="w")

        self.sembol_var = tk.StringVar(value="ASELS")
        ttk.Entry(secim_frame, textvariable=self.sembol_var, font=("Arial", 11), width=14
                  ).grid(row=0, column=1, sticky="w", padx=(8, 0))

        tk.Label(secim_frame, text="veya seç:", font=("Arial", 10), bg=self.bg_color
                 ).grid(row=0, column=2, sticky="w", padx=(18, 4))

        populer = ["ASELS", "THYAO", "GARAN", "AKBNK", "YKBNK", "EREGL", "TUPRS", "KCHOL", "BIMAS", "TTKOM"]
        self.combo = ttk.Combobox(secim_frame, values=populer, font=("Arial", 10), width=11, state="readonly")
        self.combo.grid(row=0, column=3, sticky="w")
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.sembol_var.set(self.combo.get()))

        # --- Analiz Seçenekleri ---
        opt_frame = tk.LabelFrame(main, text="📋  Analiz Seçenekleri",
                                  font=("Arial", 11, "bold"), bg=self.bg_color, padx=12, pady=8)
        opt_frame.pack(fill=tk.X, pady=(0, 12))

        self.grafik_var = tk.BooleanVar(value=True)
        self.excel_var  = tk.BooleanVar(value=True)
        self.rapor_var  = tk.BooleanVar(value=True)

        tk.Checkbutton(opt_frame, text="📊  Grafik Oluştur",  variable=self.grafik_var, font=("Arial", 10), bg=self.bg_color).grid(row=0, column=0, sticky="w", pady=2)
        tk.Checkbutton(opt_frame, text="📑  Excel Raporu",    variable=self.excel_var,  font=("Arial", 10), bg=self.bg_color).grid(row=0, column=1, sticky="w", pady=2, padx=(30,0))
        tk.Checkbutton(opt_frame, text="📝  Konsol Raporu",   variable=self.rapor_var,  font=("Arial", 10), bg=self.bg_color).grid(row=0, column=2, sticky="w", pady=2, padx=(30,0))

        # --- Butonlar ---
        btn_frame = tk.Frame(main, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=(0, 12))

        self.analiz_btn = tk.Button(btn_frame, text="🚀  Analizi Başlat",
                                    font=("Arial", 11, "bold"), bg=self.accent_color, fg="white",
                                    padx=28, pady=8, bd=0, cursor="hand2", command=self.analiz_baslat)
        self.analiz_btn.pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(btn_frame, text="📂  Klasörü Aç",
                  font=("Arial", 10), bg="#10AC84", fg="white",
                  padx=16, pady=8, bd=0, cursor="hand2", command=self.klasor_ac
                  ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(btn_frame, text="🗑️  Temizle",
                  font=("Arial", 10), bg="#95A5A6", fg="white",
                  padx=16, pady=8, bd=0, cursor="hand2", command=self.temizle
                  ).pack(side=tk.LEFT)

        tk.Button(btn_frame, text="❌  Çıkış",
                  font=("Arial", 10), bg="#EE5A6F", fg="white",
                  padx=16, pady=8, bd=0, cursor="hand2", command=self.root.quit
                  ).pack(side=tk.RIGHT)

        # --- Çıktı Alanı ---
        cikti_frame = tk.LabelFrame(main, text="📊  Durum / Çıktı",
                                    font=("Arial", 11, "bold"), bg=self.bg_color, padx=8, pady=8)
        cikti_frame.pack(fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(cikti_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.cikti_text = tk.Text(cikti_frame, height=14, font=("Consolas", 9),
                                  bg="#1e1e1e", fg="#d4d4d4", wrap=tk.WORD, yscrollcommand=scroll.set,
                                  insertbackground="white", padx=10, pady=6)
        self.cikti_text.pack(fill=tk.BOTH, expand=True)
        scroll.config(command=self.cikti_text.yview)

        # Renkli tag'lar
        self.cikti_text.tag_configure("baslik",  foreground="#569CD6", font=("Consolas", 9, "bold"))
        self.cikti_text.tag_configure("basari",  foreground="#4EC9B0")
        self.cikti_text.tag_configure("hata",    foreground="#F44747")
        self.cikti_text.tag_configure("uyari",   foreground="#FFB200")
        self.cikti_text.tag_configure("normal",  foreground="#d4d4d4")

        # İlk mesaj
        self.log("✅  Program hazır!", "basari")
        self.log(f"📁  Çalışma dizini: {os.getcwd()}", "normal")
        if not BOT_MEVCUT:
            self.log(f"⚠️  Bot bulunamadı: {IMPORT_HATA}", "hata")

    # ── Yardımcılar ──────────────────────────────────
    def log(self, mesaj, tag="normal"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.cikti_text.insert(tk.END, f"[{ts}] {mesaj}\n", tag)
        self.cikti_text.see(tk.END)
        self.cikti_text.update()

    def temizle(self):
        self.cikti_text.delete("1.0", tk.END)
        self.log("🗑️  Temizlendi.", "normal")

    def klasor_ac(self):
        try:
            os.startfile(os.getcwd())
        except:
            messagebox.showinfo("Bilgi", f"Klasör yolu:\n{os.getcwd()}")

    # ── Analiz ───────────────────────────────────────
    def analiz_baslat(self):
        sembol = self.sembol_var.get().strip().upper()
        if not sembol:
            messagebox.showwarning("Uyarı", "Lütfen bir hisse kodu girin!")
            return
        if not BOT_MEVCUT:
            messagebox.showerror("Hata",
                "Bot dosyası bulunamadı!\n\n"
                "bilanco_analiz_botu_FINAL.py dosyasını\n"
                "bu programla aynı klasöre koyun.")
            return

        self.analiz_btn.config(state=tk.DISABLED, text="⏳  Analiz yapılıyor...")
        t = threading.Thread(target=self._analiz_calistir, args=(sembol,), daemon=True)
        t.start()

    def _analiz_calistir(self, sembol):
        try:
            self.log(f"\n{'='*52}", "baslik")
            self.log(f"🚀  {sembol} analiz başlatılıyor...", "baslik")
            self.log(f"{'='*52}", "baslik")

            bot = BilancoAnalizBotu(sirket_kodu=sembol)
            bot.tum_analizleri_yap()

            # Oranlar
            self.log("\n📊  FINANSAL ORANLAR:", "baslik")
            for kategori, oranlar in bot.oranlar.items():
                self.log(f"\n  ── {kategori.upper()} ──", "baslik")
                for k, v in oranlar.items():
                    self.log(f"     {k:35s}: {v}", "normal")

            # Grafik
            if self.grafik_var.get():
                self.log("\n📊  Grafik oluşturuluyor...", "uyari")
                g = bot.trend_analizi_grafik()
                self.log(f"✅  Grafik: {os.path.basename(g)}", "basari")

            # Excel
            if self.excel_var.get():
                self.log("📑  Excel raporu oluşturuluyor...", "uyari")
                x = bot.karsilastirma_excel()
                self.log(f"✅  Excel : {os.path.basename(x)}", "basari")

            self.log(f"\n{'='*52}", "baslik")
            self.log("✅  TÜM İŞLEMLER TAMAMLANDI!", "basari")
            self.log(f"{'='*52}", "baslik")

            self.root.after(0, lambda: messagebox.showinfo(
                "Başarılı", f"✅ {sembol} analizi tamamlandı!\nDosyalar mevcut klasöre kaydedildi."))

        except Exception as e:
            self.log(f"\n❌  HATA: {e}", "hata")
            self.root.after(0, lambda: messagebox.showerror("Hata", f"Hata oluştu:\n\n{e}"))

        finally:
            self.root.after(0, lambda: self.analiz_btn.config(state=tk.NORMAL, text="🚀  Analizi Başlat"))


def main():
    root = tk.Tk()
    app = BilancoAnalizGUI(root)
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    root.mainloop()


if __name__ == "__main__":
    main()