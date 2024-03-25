import io
import os
import shutil
from typing import Optional
import logging

import cv2
from fastapi import FastAPI, File, UploadFile, Form
from starlette.responses import StreamingResponse


logging.basicConfig(level=logging.DEBUG)
app = FastAPI()


@app.get("/")
def test_root():
    return {"Hello": "World"}


@app.post("/salam2")
def test_2(name: str = Form(...)):
    return "علیک سلام" + " " + name


@app.post("/gray")
def rgb2gray(input_image_file: UploadFile = File(...)):
    user_id = '1'
    os.makedirs(f'io/{user_id}', exist_ok=True)

    # save image file
    extension = input_image_file.filename.split('.')[-1]
    input_image_file.filename = f"input_image.{extension}"
    input_image_file_path = f"io/{user_id}/{input_image_file.filename}"
    with open(input_image_file_path, "wb") as buffer:
        shutil.copyfileobj(input_image_file.file, buffer)
    logging.debug(f"image saved for user id:{user_id}")

    # Crop and align the images
    logging.info(f"convert color image to gray for user id:{user_id}")

    image_color = cv2.imread(input_image_file_path)
    image_gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(input_image_file_path, image_gray)  # optional
    logging.debug(f"image writed for user id:{user_id}")

    _, final_image = cv2.imencode(".jpg", image_gray)
    shutil.rmtree(f'io/{user_id}')
    return StreamingResponse(io.BytesIO(final_image.tobytes()), media_type="image/jpg")
