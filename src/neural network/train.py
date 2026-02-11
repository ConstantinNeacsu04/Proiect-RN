import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from model import build_model
import os

# CONFIGURARE
FOLDER_DATE = '../imagini antrenare' # Calea relativa
MODEL_SAVE_PATH = '../model_scule_cnc.keras'
BATCH_SIZE = 32
EPOCHS = 10

def start_training():
    # 1. Pregatire Date
    train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2,
                                       rotation_range=15, horizontal_flip=True)

    train_generator = train_datagen.flow_from_directory(
        FOLDER_DATE, target_size=(224, 224), batch_size=BATCH_SIZE,
        class_mode='categorical', subset='training')

    val_generator = train_datagen.flow_from_directory(
        FOLDER_DATE, target_size=(224, 224), batch_size=BATCH_SIZE,
        class_mode='categorical', subset='validation')

    # 2. Construire Model
    print("🏗️ Construiesc modelul...")
    model = build_model(num_classes=2)

    # 3. Antrenare
    print("🚀 Încep antrenarea...")
    history = model.fit(train_generator, epochs=EPOCHS, validation_data=val_generator)

    # 4. Salvare
    model.save(MODEL_SAVE_PATH)
    print(f"✅ Model salvat: {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    start_training()