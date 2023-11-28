import streamlit as st
import requests

# Streamlit code for file upload
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the selected image
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

    # Make a request to the FastAPI endpoint for prediction
    # Replace 'http://your-fastapi-server:8000' with the actual address of your FastAPI server
    url = "https://myfirstapp-front.streamlit.app/predict"
    files = {"file": uploaded_file}
    
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Display the prediction
        st.json(response.json())
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error making prediction request: {e}")
