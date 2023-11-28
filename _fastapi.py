from fastapi import FastAPI, UploadFile, HTTPException
from tensorflow.keras.models import load_model
import numpy as np
import io
from PIL import Image

app = FastAPI()

@app.get("/")
def greet():
    return {"message": "bonjour"}


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
    try:
        print("Received image.")
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
        print("Prediction successful.")

        return {"predictions": rec}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
