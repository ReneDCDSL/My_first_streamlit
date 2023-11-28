import streamlit as st
from PIL import Image
import requests
import json  # Ensure the json module is imported

st.title("Poubelle Intelligente")

upload = st.file_uploader("Chargez l'image de votre objet", type=['png', 'jpeg', 'jpg'])

c1, c2 = st.columns(2)

if upload:
    files = {"file": (upload.name, upload.read(), upload.type)}
    req = requests.post("https://myfirstapp-front.streamlit.app/predict", files=files)  # Assuming FastAPI is running locally
    
    if req.status_code == 200:
        print(req.content)  # Print the raw content of the response
        print(req.status_code)
        print(req.text)
        try:
            resultat = req.json()
            print(resultat)
            rec = resultat["predictions"]
            prob_recyclable = rec * 100
            prob_organic = (1 - rec) * 100

            c1.image(Image.open(upload))
            if prob_recyclable > 50:
                c2.write(f"Je suis certain à {prob_recyclable:.2f} % que l'objet est recyclable")
            else:
                c2.write(f"Je suis certain à {prob_organic:.2f} % que l'objet n'est pas recyclable")
        except json.JSONDecodeError:
            print("Response is not valid JSON.")
            # Handle non-JSON response here
    else:
        print(f"Request failed with status code: {req.status_code}")
