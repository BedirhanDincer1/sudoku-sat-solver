import tkinter as tk
from tkinter import messagebox, filedialog # Kullanıcının dosya seçmesi (file dialog) ve uyarı mesajları için

class SudokuApp:
    def __init__(self, root, solver_callback, ocr_callback):
        """
        Uygulamanın başlangıç fonksiyonu (Constructor).
        
        Parametreler:
        - root: Ana pencere nesnesi (Tkinter'dan gelir).
        - solver_callback: 'ÇÖZ' butonuna basınca çalışacak dış fonksiyon (main.py'den gelecek).
        - ocr_callback: 'RESİM YÜKLE' butonuna basınca çalışacak dış fonksiyon (main.py'den gelecek).
        """
        self.root = root
        self.root.title("Yapay Zeka Sudoku Çözücü")
        
        # --- Dependency Injection (Bağımlılık Enjeksiyonu) ---
        # GUI sınıfı, SAT çözücünün veya OCR'ın nasıl çalıştığını bilmez.
        # Sadece kendisine verilen fonksiyonları tetikler.
        self.solver_callback = solver_callback 
        self.ocr_callback = ocr_callback 
        
        # Ekrandaki 81 adet kutucuğu (Entry widget) sonradan erişebilmek için 
        # (satır, sütun) koordinatlarıyla bu sözlükte saklayacağız.
        self.cells = {} 
        
        # Arayüz elemanlarını ekrana yerleştir
        self._setup_ui()

    def _setup_ui(self):
        """Arayüzün tasarımını (butonlar, grid yapısı) oluşturan fonksiyon."""
        
        # --- 1. ÜST PANEL: Resim Yükleme ---
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack() # Paneli pencereye yerleştir
        
        # Resim yükleme butonu
        load_btn = tk.Button(top_frame, text="📁 SUDOKU RESMİ YÜKLE", 
                             command=self.load_image_action, # Tıklanınca bu fonksiyon çalışır
                             bg="#2196F3", fg="white", font=('Arial', 10, 'bold'))
        load_btn.pack()

        # --- 2. ORTA PANEL: Sudoku Izgarası (Grid) ---
        grid_frame = tk.Frame(self.root, padx=10, pady=10)
        grid_frame.pack()

        # 9x9'luk döngü ile kutucukları oluşturuyoruz
        for i in range(9):
            for j in range(9):
                # --- Görsel Ayraç Mantığı ---
                # Sudoku'nun 3x3'lük bloklarını belli etmek için
                # her 3 satırda ve 3 sütunda bir boşluğu (padding) artırıyoruz.
                pad_top = 5 if i % 3 == 0 and i != 0 else 1
                pad_left = 5 if j % 3 == 0 and j != 0 else 1
                
                # Entry: Kullanıcının sayı girebildiği kutucuk
                cell = tk.Entry(grid_frame, width=3, font=('Arial', 18), justify='center')
                
                # Grid sistemi ile kutucuğu yerine koyuyoruz
                cell.grid(row=i, column=j, padx=(pad_left, 1), pady=(pad_top, 1))
                
                # Kutucuğu sözlüğe kaydet ki sonra içindeki sayıyı okuyabilelim
                self.cells[(i, j)] = cell

        # --- 3. ALT PANEL: Aksiyon Butonları ---
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack()

        # Çözme butonu
        solve_btn = tk.Button(btn_frame, text="✅ SAT İLE ÇÖZ", command=self.solve_action, 
                              bg="#4CAF50", fg="white", font=('Arial', 12, 'bold'))
        solve_btn.pack(side=tk.LEFT, padx=10)

        # Temizleme butonu
        clear_btn = tk.Button(btn_frame, text="TEMİZLE", command=self.clear_grid,
                              bg="#f44336", fg="white", font=('Arial', 12))
        clear_btn.pack(side=tk.LEFT, padx=10)

    def load_image_action(self):
        """Kullanıcı 'Resim Yükle'ye basınca çalışır."""
        
        # İşletim sisteminin dosya seçme penceresini açar
        file_path = filedialog.askopenfilename(
            title="Bir Sudoku Resmi Seçin",
            filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg")]
        )
        
        # Eğer kullanıcı bir dosya seçip 'Tamam' dediyse:
        if file_path:
            try:
                # 1. Main.py'den gelen OCR fonksiyonunu çalıştır
                # Bu fonksiyon resim yolunu alıp bize 9x9 sayı matrisi (liste) döner
                detected_grid = self.ocr_callback(file_path)
                
                # 2. Önce ekranı temizle
                self.clear_grid()
                
                # 3. Bulunan sayıları ekrana yaz
                self.update_grid(detected_grid)
                
                # 4. Bilgi mesajı ver
                messagebox.showinfo("Başarılı", "Resim tarandı ve sayılar yerleştirildi!")
                
            except Exception as e:
                # OCR sırasında hata olursa kullanıcıya göster
                messagebox.showerror("OCR Hatası", f"Resim okunamadı:\n{e}")

    def get_grid_values(self):
        """
        Arayüzdeki (GUI) kutucuklarda yazan değerleri okur ve
        SAT çözücünün anlayacağı 9x9'luk tamsayı listesine çevirir.
        """
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                # Kutucuktan veriyi al (string olarak gelir)
                val = self.cells[(i, j)].get()
                
                # Eğer sayı girilmişse integer'a çevir, boşsa 0 yap
                if val.isdigit():
                    row.append(int(val))
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def update_grid(self, grid_data):
        """
        Dışarıdan gelen 9x9'luk sayı matrisini arayüze yazar.
        OCR sonucu veya Çözüm sonucu göstermek için kullanılır.
        """
        for i in range(9):
            for j in range(9):
                val = grid_data[i][j]
                
                # Sadece değeri 0 olmayan (dolu) hücreleri yaz
                if val != 0:
                    # Önce kutucuğun içini temizle
                    self.cells[(i, j)].delete(0, tk.END)
                    # Yeni değeri yaz
                    self.cells[(i, j)].insert(0, str(val))
                    
                    # Sayıları mavi renk yap (Görsel geri bildirim)
                    self.cells[(i, j)].config(fg="blue")

    def clear_grid(self):
        """Tüm kutucukları temizler ve rengi sıfırlar."""
        for cell in self.cells.values():
            cell.delete(0, tk.END)
            cell.config(fg="black") # Rengi siyaha döndür

    def solve_action(self):
        """ 'SAT İLE ÇÖZ' butonuna basılınca çalışır."""
        try:
            # 1. Ekrandaki mevcut durumu oku
            current_grid = self.get_grid_values()
            
            # 2. Main.py'den gelen çözücü fonksiyonunu çağır
            solved_grid = self.solver_callback(current_grid)
            
            # 3. Eğer çözüm başarılıysa ekrana yaz
            if solved_grid:
                self.update_grid(solved_grid)
            else:
                messagebox.showwarning("Sonuç", "Bu Sudoku için çözüm bulunamadı!")
                
        except Exception as e:
            messagebox.showerror("Hata", str(e))
