import tensorflow as tf
from tensorflow.keras.utils import plot_model

def deseneaza_arhitectura():
    try:
        model = tf.keras.models.load_model('../model_scule_cnc.keras')
        
        # Salveaza o poza cu schema bloc a retelei
        plot_model(model, to_file='arhitectura_model.png', 
                   show_shapes=True, 
                   show_layer_names=True)
        print("✅ Imaginea 'arhitectura_model.png' a fost generată.")
    except Exception as e:
        print(f"Eroare (posibil lipsește graphviz): {e}")
        model.summary() # Măcar printează textul

if __name__ == "__main__":
    deseneaza_arhitectura()