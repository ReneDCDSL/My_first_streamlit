import streamlit as st
from PIL import Image
import requests
import json

st.title("Poubelle Intelligente")

c1, c2 = st.columns(2)

# Streamlit code for file upload
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])

# Initialize variables
prob_recyclable, prob_organic = 0, 0

if uploaded_file is not None:
    # Display the selected image
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

    # Make a request to the FastAPI endpoint for prediction
    url = "https://myfirstapp-v3.streamlit.app/predict"
    files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}

    response = requests.post(url, files=files)

    try:
        resultat = response.json()
        print(resultat)
        rec = resultat["predictions"]
        prob_recyclable = rec * 100
        prob_organic = (1 - rec) * 100

    except json.JSONDecodeError:
        st.error(f"Invalid JSON received from the server. Response content: {response.json}")
    except Exception as e:
        st.error(f"Error: {str(e)}")

    c1.image(Image.open(uploaded_file))
    if prob_recyclable > 50:
        c2.write(f"Je suis certain à {prob_recyclable:.2f} % que l'objet est recyclable")
    else:
        c2.write(f"Je suis certain à {prob_organic:.2f} % que l'objet n'est pas recyclable")
