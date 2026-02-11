import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import os

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(
    page_title="Proiect RN",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS PENTRU DESIGN INDUSTRIAL & VIZIBILITATE ---
st.markdown("""
    <style>
    /* A. FUNDAL GENERAL ȘI TEXT PRINCIPAL (Aici era problema) */
    .stApp {
        background-color: #1E1E1E;
    }
    
    /* Forțăm TOT textul din aplicație să fie alb/gri deschis */
    p, div, label, h1, h2, h3, h4, h5, h6, span {
        color: #E0E0E0 !important;
    }

    /* B. SIDEBAR (Meniul din stânga) */
    [data-testid="stSidebar"] {
        background-color: #252526;
        border-right: 1px solid #3E3E42;
    }
    
    /* C. BUTOANE ȘI WIDGET-URI */
    .stButton>button {
        background-color: #007ACC;
        color: white !important;
        border: 1px solid #005A9E;
        font-weight: bold;
        width: 100%;
        border-radius: 0px;
    }
    
    /* Zona de Upload (Să se vadă clar chenarul) */
    [data-testid="stFileUploader"] {
        background-color: #2D2D2D;
        padding: 20px;
        border: 1px dashed #444;
        border-radius: 5px;
    }

    /* D. BOX-URI DE STATUS */
    .success-box {
        padding: 20px;
        background-color: #1B5E20; 
        border: 2px solid #4CAF50;
        margin-bottom: 10px;
        text-align: center;
    }
    .error-box {
        padding: 20px;
        background-color: #B71C1C;
        border: 2px solid #FF5252;
        margin-bottom: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNCȚII ---

@st.cache_resource
def incarca_model():
    path_model = 'model_scule_cnc.keras'
    if not os.path.exists(path_model):
        return None
    try:
        model = tf.keras.models.load_model(path_model)
        return model
    except:
        return None

def preprocesare_imagine(image_data):
    size = (224, 224)
    image = ImageOps.fit(image_data, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 255.0)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    return data, image

# --- 4. INTERFAȚA ---

st.title("Sistem de detectare a uzurii frezelor CNC")

# Sidebar
with st.sidebar:
    st.header("Panou control")
    st.info("Sistem pregatit") # Acum se va vedea bine
    
    st.markdown("### Configurare")
    confidence_threshold = st.slider("Sensibilitate (%)", 0, 100, 50)
    
    st.markdown("### Informatii Opretator")
    st.text("User: OPERATOR_1")
    
    
    st.markdown("---")
    st.caption("v2.1.0 | Model: MobileNetV2")

# Încărcare
model = incarca_model()

if model is None:
    st.markdown("""
        <div class="error-box">
            <h3 style="color:white;"> Eroare </h3>
            <p>MODEL FILE NOT FOUND: 'model_scule_cnc.keras'</p>
        </div>
    """, unsafe_allow_html=True)
else:
    # Aici este partea care dispăruse (acum e albă pe fundal gri)
    file = st.file_uploader("Incarcare fisier (JPG/PNG)", type=["jpg", "png", "jpeg"])

    if file:
        col1, col2 = st.columns([1, 2])
        
        # Procesare
        data, image_preview = preprocesare_imagine(Image.open(file))
        prediction = model.predict(data)
        score_neconform = prediction[0][1] 
        score_conform = prediction[0][0]
        
        with col1:
            st.image(image_preview, caption="Imagine", use_container_width=True)

        with col2:
            st.subheader("Rezultat")
            
            if score_neconform > (confidence_threshold / 100):
                st.markdown(f"""
                    <div class="error-box">
                        <h2 style="color:white; margin:0;"> NECONFORM</h2>
                        <p style="font-size:18px;">DEFECT CRITIC</p>
                    </div>
                """, unsafe_allow_html=True)
                col_m1, col_m2 = st.columns(2)
                col_m1.metric("PROBABILITATE DEFECT ", f"{score_neconform*100:.2f}%")
                col_m2.metric("ACTION", "REJECT PART")
            else:
                st.markdown(f"""
                    <div class="success-box">
                        <h2 style="color:white; margin:0;"> CONFORM</h2>
                        <p style="font-size:18px;">FREZA INCA BUNA</p>
                    </div>
                """, unsafe_allow_html=True)
                col_m1, col_m2 = st.columns(2)
                col_m1.metric("SCOR", f"{score_conform*100:.2f}%")
                col_m2.metric("ACTION", "ACCEPT PART")

            with st.expander("VIEW RAW TELEMETRY DATA"):
                st.code(f"RAW_OUTPUT: {prediction[0]}")