import streamlit as st
from PIL import Image
import requests

st.title("Poubelle Intelligente")

upload = st.file_uploader("Chargez l'image de votre objet", type=['png', 'jpeg', 'jpg'])

c1, c2 = st.columns(2)

if upload:
    files = {"file": (upload.name, upload.read(), upload.type)}
    req = requests.post("https://myfirstapp-v3.streamlit.app/predict", files=files)  # Adjust the URL if needed

    if req.status_code == 200:
        try:
            resultat = req.json()
            st.write("Received response:", resultat)  # Display the received response for debugging

            # Additional debugging to print raw response content
            st.text("Raw response content:")
            st.text(req.content)

            if "predictions" in resultat:
                rec = resultat["predictions"]
                prob_recyclable = rec * 100
                prob_organic = (1 - rec) * 100

                c1.image(Image.open(upload))
                if prob_recyclable > 50:
                    c2.write(f"Je suis certain à {prob_recyclable:.2f}% que l'objet est recyclable")
                else:
                    c2.write(f"Je suis certain à {prob_organic:.2f}% que l'objet n'est pas recyclable")
            else:
                st.error("Invalid response format from the server.")
        except ValueError:
            st.error("Invalid JSON received from the server.")
    else:
        st.error(f"Error making prediction request. Server returned status code: {req.status_code}")
