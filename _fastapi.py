from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
import numpy as np
import io
from PIL import Image

app = FastAPI()

# Replace "https://myfirstapp-v3.streamlit.app" with your actual Streamlit app domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myfirstapp-v3.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load():
    model_path = "best_model.h5"
    model = load_model(model_path, compile=False)
    return model

# Chargement du model
model = load()

def preprocess(img):
    img = img.resize((224, 224))
    img = np.asarray(img)
    img = np.expand_dims(img, axis=0)
    return img

@app.post("/predict")
async def predict(file: UploadFile):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    image_data = await file.read()

    # open the image
    img = Image.open(io.BytesIO(image_data))

    # preprocessing
    img_processed = preprocess(img)

    # prediction
    predictions = model.predict(img_processed)
    rec = predictions[0][0].tolist()

    return {"predictions": rec}
