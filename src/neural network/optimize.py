import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers

MODEL_PATH = '../model_scule_cnc.keras'
DATA_PATH = '../imagini antrenare'

def fine_tune():
    print("🔧 Încep optimizarea (Fine-Tuning)...")
    
    # 1. Incarcam modelul existent
    model = load_model(MODEL_PATH)
    
    # 2. "Dezghetam" baza MobileNet
    base_model = model.layers[0]
    base_model.trainable = True
    
    # 3. Re-compilam cu Learning Rate FOARTE MIC
    model.compile(optimizer=optimizers.Adam(1e-5),  # 0.00001
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    # 4. Antrenam inca putin (Fine Tuning)
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    train_gen = datagen.flow_from_directory(DATA_PATH, target_size=(224,224), subset='training')
    val_gen = datagen.flow_from_directory(DATA_PATH, target_size=(224,224), subset='validation')
    
    model.fit(train_gen, epochs=5, validation_data=val_gen)
    
    # 5. Salvam versiunea optimizata
    model.save('../model_scule_cnc_OPTIMIZAT.keras')
    print("✅ Modelul optimizat a fost salvat!")

if __name__ == "__main__":
    fine_tune()