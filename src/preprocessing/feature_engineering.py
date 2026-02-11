import os
from PIL import Image, ImageOps

INPUT_FOLDER = '../imagini antrenare'
OUTPUT_FOLDER = '../imagini procesate' # Se va crea automat

def preprocesare_features():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        
    print("⚙️ Încep extragerea și standardizarea imaginilor...")
    
    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Calea veche
                path_in = os.path.join(root, file)
                
                # Pastram structura folderelor (Conform/Neconform)
                rel_path = os.path.relpath(root, INPUT_FOLDER)
                path_out_dir = os.path.join(OUTPUT_FOLDER, rel_path)
                
                if not os.path.exists(path_out_dir):
                    os.makedirs(path_out_dir)
                
                # Procesare: Resize la 224x224 (Standard MobileNet)
                try:
                    img = Image.open(path_in)
                    # Resize inteligent (fără deformare)
                    img = ImageOps.fit(img, (224, 224), Image.Resampling.LANCZOS)
                    
                    # Salvare in noul folder
                    path_out = os.path.join(path_out_dir, file)
                    img.save(path_out)
                except Exception as e:
                    print(f"Eroare la {file}: {e}")

    print(f"✅ Imaginile procesate au fost salvate în '{OUTPUT_FOLDER}'")

if __name__ == "__main__":
    preprocesare_features()