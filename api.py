import streamlit as st
from PIL import Image
import requests
import json

st.title("Poubelle Intelligente")

upload = st.file_uploader("Chargez l'image de votre objet", type=['png', 'jpeg', 'jpg'])

c1, c2 = st.columns(2)

if upload:
    files = {"file": (upload.name, upload.read(), upload.type)}
    req = requests.post("https://myfirstapp-front.streamlit.app/predict", files=files)  # Assuming FastAPI is running locally

    try:
        req.raise_for_status()
        resultat = req.json()
        print(resultat)  # Print the response for debugging
        rec = resultat["predictions"]
        prob_recyclable = rec * 100
        prob_organic = (1 - rec) * 100

        c1.image(Image.open(upload))
        if prob_recyclable > 50:
            c2.write(f"Je suis certain à {prob_recyclable:.2f} % que l'objet est recyclable")
        else:
            c2.write(f"Je suis certain à {prob_organic:.2f} % que l'objet n'est pas recyclable")

    except requests.HTTPError as err:
        st.error(f"HTTP error occurred: {err}")
        st.text(req.text)  # Print the actual response text
    except json.decoder.JSONDecodeError:
        st.error("Invalid JSON response:")
        st.text(req.text)  # Print the actual response text
    

# Display the prediction
st.json(response.json())  # Assuming 'response' is the variable holding the FastAPI response
