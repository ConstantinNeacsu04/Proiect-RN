import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

# --- CONFIGURARE FINALĂ ---
# Mergem direct la sursă, unde știm sigur că ai pozele (în Users)
FOLDER_TINTA = r'C:\Users\Cristian NCS\dataset_local\conform'
NUMAR_COPII = 1  # Dublare (1 copie per poză)

print("\n--- PORNIRE GENERATOR ---")
print(f"🔍 Caut pozele în: {FOLDER_TINTA}")

# Verificare de siguranță
if not os.path.exists(FOLDER_TINTA):
    print("\n❌ EROARE GRAVĂ: Folderul nu este nici aici!")
    print("   Verifică manual dacă în 'C:\\Users\\Cristian NCS\\dataset_local' există un folder 'conform'.")
    raise SystemExit()

# Căutare imagini
extensii = ('.jpg', '.jpeg', '.png', '.bmp')
fisiere = [f for f in os.listdir(FOLDER_TINTA) if f.lower().endswith(extensii)]
fisiere_originale = [f for f in fisiere if not f.startswith('aug_')]

print(f"📸 Am găsit {len(fisiere_originale)} imagini originale.")

if len(fisiere_originale) == 0:
    print("⚠️ Nu am găsit poze originale de dublat.")
    raise SystemExit()

# Configurare transformări
datagen = ImageDataGenerator(
    rotation_range=20, width_shift_range=0.1, height_shift_range=0.1,
    zoom_range=0.1, horizontal_flip=True, fill_mode='nearest'
)

print(f"⚙️  Generez copiile...")
total_generate = 0

for nume_fisier in fisiere_originale:
    try:
        cale_poza = os.path.join(FOLDER_TINTA, nume_fisier)
        img = load_img(cale_poza)
        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)

        i = 0
        for batch in datagen.flow(x, batch_size=1,
                                  save_to_dir=FOLDER_TINTA,
                                  save_prefix='aug_' + nume_fisier.split('.')[0],
                                  save_format='jpg'):
            i += 1
            total_generate += 1
            if i >= NUMAR_COPII:
                break
    except Exception as e:
        print(f"⚠️ Eroare la {nume_fisier}: {e}")

print("\n" + "="*40)
print(f"✅ GATA! Am pus {total_generate} poze noi în C:\\Users\\Cristian NCS\\...")
print("IMPORTANT: Pentru antrenare, va trebui să muți tot folderul 'dataset_local' pe Desktop.")
print("="*40)