import io
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse


app = FastAPI()
friends = {}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def get_items():
    return friends


@app.post("/items")
def add_item(id: str = Form(), name: str = Form(), age: float = Form()):
    friends[id] = {"name": name, "age": age}
    return friends[id]


@app.put("/items/{id}")
def update_item(id: str, name: str = Form(None), age: float = Form(None)):
    if id not in friends:
        raise HTTPException(status_code=404, detail="Item not found")
    if name is not None:
        friends[id]["name"] = name
    if age is not None:
        friends[id]["age"] = age
    return friends[id]


@app.delete("/items/{id}")
def delete_item(id: str):
    if id not in friends:
        raise HTTPException(status_code=404, detail="Item not found")
    del friends[id]
    return {"message": "Item deleted"}


@app.post("/rgb2gray")
async def rgb2gray(input_file: UploadFile = File(...)):
    # Ensure that the uploaded file is an image
    if not input_file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Unsupported file type")

    contents = await input_file.read()
    np_array = np.frombuffer(contents, np.uint8)
    image_rgb = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)

    image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)

    _, image_encoded = cv2.imencode(".jpg", image_gray)
    image_bytes = image_encoded.tobytes()
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg")
