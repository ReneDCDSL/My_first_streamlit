import streamlit as st
from PIL import Image
import requests

st.title("Poubelle Intelligente")

c1, c2 = st.columns(2)

# Streamlit code for file upload
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the selected image
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

    # Make a request to the FastAPI endpoint for prediction
    # Replace 'http://your-fastapi-server:8000' with the actual address of your FastAPI server
    url = "https://myfirstapp-v3.streamlit.app/predict"
    files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}    
    
    response = requests.post(url, files=files)
    # Display the prediction
    st.json(response.json())    