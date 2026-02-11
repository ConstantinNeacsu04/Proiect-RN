import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk # Pentru afișarea imaginilor
import tensorflow as tf
import numpy as np
import os

# --- CONFIGURARE ---
IMG_SIZE = (224, 224) # Trebuie să fie la fel ca la antrenare!
CLASS_NAMES = ['CONFORM', 'NECONFORM'] # Ordinea alfabetica (verify folderele!)

class AplicatieDetectie:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector Uzură Scule CNC")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")

        # 1. Încărcare Model
        self.model = None
        self.locatie_script = os.path.dirname(os.path.abspath(__file__))
        path_model = os.path.join(self.locatie_script, 'model_scule_cnc.keras')
        
        try:
            print("⌛ Se încarcă modelul AI...")
            self.model = tf.keras.models.load_model(path_model)
            print("✅ Model încărcat!")
        except Exception as e:
            messagebox.showerror("Eroare", f"Nu găsesc fișierul 'model_scule_cnc.keras'!\nEroare: {e}")
            self.root.destroy()
            return

        # 2. Interfața Grafică
        # Titlu
        self.lbl_titlu = tk.Label(root, text="Analiză Scule CNC", font=("Arial", 20, "bold"), bg="#f0f0f0")
        self.lbl_titlu.pack(pady=20)

        # Zona Imagine
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(pady=10)
        
        # Text Rezultat
        self.lbl_rezultat = tk.Label(root, text="Aștept imagine...", font=("Arial", 18), bg="#f0f0f0")
        self.lbl_rezultat.pack(pady=10)
        
        self.lbl_procent = tk.Label(root, text="", font=("Arial", 12), bg="#f0f0f0", fg="gray")
        self.lbl_procent.pack()

        # Buton Încărcare
        self.btn_load = tk.Button(root, text="📂 Încarcă Poză", font=("Arial", 14), bg="#007bff", fg="white", 
                                  command=self.incarca_imagine, padx=20, pady=10)
        self.btn_load.pack(pady=20)

    def incarca_imagine(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagini", "*.jpg *.jpeg *.png *.bmp")])
        if not file_path:
            return

        # Afișare imagine în GUI
        try:
            img_display = Image.open(file_path)
            img_display = img_display.resize((400, 400), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img_display)
            self.canvas.create_image(200, 200, image=self.photo)
            
            # Resetare text
            self.lbl_rezultat.config(text="Se analizează...", fg="black")
            self.root.update()

            # Predicție
            self.predict(file_path)

        except Exception as e:
            messagebox.showerror("Eroare", f"Nu pot deschide imaginea: {e}")

    def predict(self, file_path):
        if self.model is None: return

        # Procesare pentru AI
        img = tf.keras.utils.load_img(file_path, target_size=IMG_SIZE)
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        # Predicție
        predictions = self.model.predict(img_array, verbose=0)
        score = tf.nn.softmax(predictions[0])
        
        idx = np.argmax(score)
        clasa = CLASS_NAMES[idx]
        procent = 100 * np.max(score)

        # Actualizare Interfață
        culoare = "green" if clasa == "CONFORM" else "red"
        
        self.lbl_rezultat.config(text=f"Verdict: {clasa}", fg=culoare)
        self.lbl_procent.config(text=f"Siguranță AI: {procent:.2f}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicatieDetectie(root)
    root.mainloop()