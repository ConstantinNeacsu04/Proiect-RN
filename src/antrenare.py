import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models, optimizers
import os

# --- CONFIGURARE ---
FOLDER_DATE = 'imagini antrenare' # Asigura-te ca ai folderele 'date conforme' si 'date neconforme' aici
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10  # Facem 10 epoci de calitate

# 1. Pregătirea Datelor (Cu Augmentare pentru a evita memorarea)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,      # Rotim putin pozele
    width_shift_range=0.2,  # Le miscam stanga-dreapta
    height_shift_range=0.2, # Le miscam sus-jos
    horizontal_flip=True,   # Le oglindim
    validation_split=0.2    # Pastram 20% pentru testare
)

print("Incarc datele de antrenare...")
train_generator = train_datagen.flow_from_directory(
    FOLDER_DATE,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

print("Incarc datele de validare...")
validation_generator = train_datagen.flow_from_directory(
    FOLDER_DATE,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# 2. Construirea Modelului (MobileNetV2)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False # Inghetam baza initial

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),  # Uităm 30% din conexiuni ca sa nu toceasca
    layers.Dense(128, activation='relu'),
    layers.Dense(2, activation='softmax') # 2 clase: Conform vs Neconform
])

# Folosim un Learning Rate mic pentru precizie
model.compile(optimizer=optimizers.Adam(learning_rate=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 3. Antrenarea
print("\n--- INCEP ANTRENAREA (Dureaza aprox 5-10 min) ---")
# Truc: class_weight nu e necesar daca augmentam datele bine, 
# dar antrenam un pic mai mult
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator
)

# 4. Salvarea
nume_final = 'model_scule_cnc.keras'
model.save(nume_final)
print(f"\n✅ GATA! Noul model a fost salvat ca '{nume_final}'.")
print("Acum poti rula din nou 'streamlit run app.py'!")