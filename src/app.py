import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import os

# --- 1. CONFIGURARE PAGINA ---
st.set_page_config(
    page_title="Proiect RN - Inspectie Scule",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS PENTRU DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #1E1E1E; }
    p, div, label, h1, h2, h3, h4, h5, h6, span, li { color: #E0E0E0 !important; }
    [data-testid="stSidebar"] { background-color: #252526; border-right: 1px solid #3E3E42; }
    .stButton>button { background-color: #007ACC; color: white !important; width: 100%; border-radius: 0px; }
    [data-testid="stFileUploader"] { background-color: #2D2D2D; padding: 20px; border: 1px dashed #444; border-radius: 5px; }
    .success-box { padding: 20px; background-color: #1B5E20; border: 2px solid #4CAF50; margin-bottom: 10px; text-align: center; border-radius: 5px; }
    .error-box { padding: 20px; background-color: #B71C1C; border: 2px solid #FF5252; margin-bottom: 10px; text-align: center; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNCTII ---

@st.cache_resource
def incarca_model():
    path_model = 'model_scule_cnc.keras'
    if not os.path.exists(path_model):
        return None
    try:
        model = tf.keras.models.load_model(path_model)
        return model
    except Exception as e:
        st.error(f"Eroare la incarcarea modelului: {e}")
        return None

def preprocesare_imagine(image_data):
    # --- MODIFICARE CRITICA: Exact ca in testare.py ---
    
    # 1. Dimensiunea CORECTA (Modelul tau vrea 224, nu 180)
    size = (224, 224) 
    image = ImageOps.fit(image_data, size, Image.Resampling.LANCZOS)
    
    # 2. Convertim in array
    image_array = np.asarray(image)
    
    # 3. NU IMPARTIM LA 255! (Aceasta era greseala care strica predictiile)
    # Modelul are un strat intern de Rescaling care asteapta valori 0-255
    image_array = image_array.astype(np.float32)
    
    # 4. Adaugam dimensiunea batch-ului (1, 224, 224, 3)
    data = np.expand_dims(image_array, axis=0)
    
    return data, image

# --- 4. INTERFATA ---

st.title("Sistem Automat de Detectare Uzura - CNC")

with st.sidebar:
    st.header("Panou Control")
    st.info("Status: ONLINE")
    confidence_threshold = st.slider("Prag Sensibilitate (%)", 0, 100, 50)
    st.markdown("---")
    st.caption("v3.1.0 | Fix: Size 224 & No Norm")

model = incarca_model()

if model is None:
    st.markdown("""<div class="error-box"><h3> EROARE CRITICA </h3><p>Lipsa fisier model!</p></div>""", unsafe_allow_html=True)
else:
    file = st.file_uploader("Incarca imaginea sculei (JPG/PNG)", type=["jpg", "png", "jpeg"])

    if file:
        col1, col2 = st.columns([1, 2])
        
        # Procesare
        data, image_preview = preprocesare_imagine(Image.open(file))
        
        # Predicție
        predictions = model.predict(data)
        score = tf.nn.softmax(predictions[0]).numpy()
        
        # --- LOGICA INDEX ---
        # Index 0 = CONFORM
        # Index 1 = NECONFORM
        prob_conform = score[0]
        prob_neconform = score[1]
        
        # Afisare imagine
        with col1:
            st.image(image_preview, caption="Imagine Analizata", use_container_width=True)

        # Afisare Rezultate
        with col2:
            st.subheader("Rezultat Analiza AI")
            
            # Verificam cine are scorul cel mai mare
            index_castigator = np.argmax(score)
            
            # Daca castiga Index 1 => NECONFORM
            if index_castigator == 1:
                st.markdown(f"""
                    <div class="error-box">
                        <h2 style="color:white; margin:0;"> NECONFORM</h2>
                        <p style="font-size:18px;">DEFECT DETECTAT</p>
                    </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                c1.metric("Siguranta AI", f"{prob_neconform*100:.2f}%")
                c2.metric("Actiune", "INLOCUIRE")
                
            else:
                # Daca castiga Index 0 => CONFORM
                st.markdown(f"""
                    <div class="success-box">
                        <h2 style="color:white; margin:0;"> CONFORM</h2>
                        <p style="font-size:18px;">SCULA ESTE BUNA</p>
                    </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                c1.metric("Siguranta AI", f"{prob_conform*100:.2f}%")
                c2.metric("Actiune", "UTILIZARE")

            # Debug
            with st.expander("Vezi datele brute (Debug)"):
                st.write(f"Index 0 (Conform): {prob_conform:.4f}")
                st.write(f"Index 1 (Neconform): {prob_neconform:.4f}")
