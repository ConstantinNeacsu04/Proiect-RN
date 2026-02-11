import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix

MODEL_PATH = '../model_scule_cnc.keras'
DATA_PATH = '../imagini antrenare' # Sau '../imagini testare reala' daca ai facut split-ul

def evalueaza_model():
    # Incarcare model
    model = load_model(MODEL_PATH)
    
    # Generator pentru test (FARA shuffle, ca sa stim ordinea)
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        DATA_PATH, target_size=(224, 224), shuffle=False, 
        batch_size=32, class_mode='categorical')

    # Predictii
    print("🔍 Generez predicții...")
    Y_pred = model.predict(test_generator)
    y_pred = np.argmax(Y_pred, axis=1)
    y_true = test_generator.classes

    # Raport
    print("\n--- RAPORT CLASIFICARE ---")
    print(classification_report(y_true, y_pred, target_names=test_generator.class_indices.keys()))
    
    # Matrice Confuzie Simpla
    print("\n--- MATRICE CONFUZIE ---")
    print(confusion_matrix(y_true, y_pred))

if __name__ == "__main__":
    evalueaza_model()