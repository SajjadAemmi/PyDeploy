import io
from typing import List, Tuple
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from src.face_analysis import FaceAnalysis

app = FastAPI()

face_analysis = FaceAnalysis("models/det_10g.onnx", "models/genderage.onnx")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/analyze-face/")
async def analyze_face(file: UploadFile = File(...)):
    # Read the uploaded image file
    image_data = await file.read()
    np_array = np.frombuffer(image_data, np.uint8)
    input_image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    # Perform face analysis
    # output_image, genders, ages = face_analysis(input_image)
    output_image, genders, ages = face_analysis.detect_age_gender(input_image)
    
    # Encode output image to JPEG
    # _, encoded_image = cv2.imencode('.jpg', output_image)
    # output_image_bytes = io.BytesIO(encoded_image.tobytes())
    
    # Create JSON response
    response_data = {
        "genders": genders,
        "ages": ages
    }
    
    return JSONResponse(content=response_data)

@app.get("/output-image/")
async def get_output_image(file: UploadFile = File(...)):
    # Read the uploaded image file
    image_data = await file.read()
    np_array = np.frombuffer(image_data, np.uint8)
    input_image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    # Perform face analysis
    output_image, _, _ = face_analysis(input_image)
    
    # Encode output image to JPEG
    _, encoded_image = cv2.imencode('.jpg', output_image)
    output_image_bytes = io.BytesIO(encoded_image.tobytes())
    
    return StreamingResponse(output_image_bytes, media_type="image/jpeg")
