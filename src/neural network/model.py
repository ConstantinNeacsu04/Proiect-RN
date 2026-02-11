import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models

def build_model(input_shape=(224, 224, 3), num_classes=2, learning_rate=0.0001):
    """
    Construiește arhitectura modelului bazată pe MobileNetV2.
    """
    # 1. Baza pre-antrenată (Transfer Learning)
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)
    base_model.trainable = False  # Înghețăm cunoștințele de bază

    # 2. Capul modelului (Partea care învață sculele tale)
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),  # Previne memorarea mecanică
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])

    # 3. Compilarea
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

if __name__ == "__main__":
    model = build_model()
    model.summary()
    print("✅ Arhitectura modelului a fost definită corect.")