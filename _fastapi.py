from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
import numpy as np
import io
from PIL import Image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Increase the upload size limit to 500MB (adjust as needed)
app = FastAPI(upload_max_size=500 * 1024 * 1024)

# Load the model
def load():
    model_path = "best_model.h5"
    model = load_model(model_path, compile=False)
    return model

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
