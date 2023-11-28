import streamlit as st
from PIL import Image
import requests

st.title("Poubelle Intelligente")

c1, c2 = st.columns(2)

# Streamlit code for file upload
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])

prob_recyclable = 0  # Initialize variables before try block
prob_organic = 0

if uploaded_file is not None:
    # Display the selected image
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

    # Make a request to the FastAPI endpoint for prediction
    # Replace 'http://your-fastapi-server:8000' with the actual address of your FastAPI server
    url = "https://myfirstapp-v3.streamlit.app/predict"
    files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}    
    
    response = requests.post(url, files=files)
    st.write("Response content:", response.content)
    
    try:
        resultat = response.json()
        print(resultat)
        rec = resultat["predictions"]
        prob_recyclable = rec * 100      
        prob_organic = (1-rec) * 100

    except requests.exceptions.JSONDecodeError as json_error:
        st.error(f"JSON Decode Error: {json_error}")
    except KeyError as key_error:
        st.error(f"Key Error: {key_error}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        
    c1.image(Image.open(uploaded_file))
    if prob_recyclable > 50:
        c2.write(f"Je suis certain à {prob_recyclable:.2f} % que l'objet est recyclable")
    else:
        c2.write(f"Je suis certain à {prob_organic:.2f} % que l'objet n'est pas recyclable")
