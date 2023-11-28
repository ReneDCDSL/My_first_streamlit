import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import io

# Load your model
model_path = "best_model.h5"
model = load_model(model_path, compile=False)

st.title("Poubelle Intelligente")

upload = st.file_uploader("Chargez l'image de votre objet", type=['png', 'jpeg', 'jpg'])

c1, c2 = st.columns(2)

if upload:
    # Preprocess the image
    img = Image.open(upload)
    img = img.resize((224, 224))
    img = np.asarray(img)
    img = np.expand_dims(img, axis=0)

    # Make prediction
    predictions = model.predict(img)
    rec = predictions[0][0].tolist()
    
    prob_recyclable = rec * 100      
    prob_organic = (1 - rec) * 100

    c1.image(Image.open(upload))
    if prob_recyclable > 50:
        c2.write(f"Je suis certain à {prob_recyclable:.2f} % que l'objet est recyclable")
    else:
        c2.write(f"Je suis certain à {prob_organic:.2f} % que l'objet n'est pas recyclable")
