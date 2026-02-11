import os
from PIL import Image

# Configurare
FOLDER_DATE = '../imagini antrenare' # ".." inseamna ca iese din folderul curent si cauta in cel mare

def curata_dataset():
    print(f"🧹 Încep curățenia în folderul: {FOLDER_DATE}")
    sterse = 0
    
    # Parcurgem toate subfolderele (Conform / Neconform)
    for root, dirs, files in os.walk(FOLDER_DATE):
        for file in files:
            cale_fisier = os.path.join(root, file)
            try:
                # Încercăm să deschidem imaginea
                img = Image.open(cale_fisier)
                img.verify() # Verificăm integritatea
            except (IOError, SyntaxError) as e:
                print(f"❌ Fișier corupt găsit: {file} -> ÎL ȘTERG.")
                os.remove(cale_fisier)
                sterse += 1
                
    print(f"✅ Gata! Am șters {sterse} fișiere corupte.")

if __name__ == "__main__":
    curata_dataset()