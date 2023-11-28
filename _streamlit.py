import streamlit as st
from PIL import Image
import requests

st.title("Poubelle Intelligente")

upload = st.file_uploader("Chargez l'image de votre objet", type=['png', 'jpeg', 'jpg'])

c1, c2 = st.columns(2)

if upload:
    files = {"file": (upload.name, upload.read(), upload.type)}
    req = requests.post("https://myfirstapp-v3.streamlit.app/predict", files=files)

    if req.status_code == 200:
        try:
            resultat = req.json()
            rec = resultat["predictions"]
            prob_recyclable = rec * 100
            prob_organic = (1 - rec) * 100

            c1.image(Image.open(upload))
            if prob_recyclable > 50:
                c2.write(f"Je suis certain à {prob_recyclable:.2f}% que l'objet est recyclable")
            else:
                c2.write(f"Je suis certain à {prob_organic:.2f}% que l'objet n'est pas recyclable")
        except ValueError:
            st.error("Invalid response from the server. Please try again.")
    else:
        st.error("Error making prediction request. Please try again.")
