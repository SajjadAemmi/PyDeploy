import io
from fastapi import FastAPI, UploadFile, HTTPException
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image as PILImage
import numpy as np


app = FastAPI()

base_options = python.BaseOptions(model_asset_path="gesture_recognizer.task")
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)


@app.get("/")
def root():
    return {"Hello": "Gesture 👋"}


@app.post("/auth/gesture")
async def gesture(file: UploadFile):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    image_data = await file.read()

    try:
        pil_image = PILImage.open(io.BytesIO(image_data)).convert("RGB")
        image_array = np.array(pil_image)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_array)

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to process image: {str(e)}"
        )
    
    try:
        # Perform gesture recognition
        recognition_result = recognizer.recognize(image)

        # Extract the top recognized gesture
        if not recognition_result.gestures or not recognition_result.gestures[0]:
            raise HTTPException(status_code=400, detail="No gesture recognized.")

        top_gesture = recognition_result.gestures[0][0]
        return {"gesture": top_gesture.category_name, "score": top_gesture.score}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Gesture recognition failed: {str(e)}"
        )
