from typing import Union
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
import uvicorn
import cv2
import numpy as np
import io

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/salam")
def test_1():
    return "علیک سلام"


@app.get("/salam/{name}")
def test_2(name: str):
    return "علیک سلام" + " " + name + " جان"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/image/{red}/{green}/{blue}")
def create_image(red: int, green: int, blue: int):

    if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255:
        image = np.zeros((200, 300, 3), dtype=np.uint8)
        image[:, :] = [blue, green, red]
        _, img_png = cv2.imencode('.png', image)
        image_bytes = img_png.tobytes()
        return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Numbers must be between 0 and 255")


if __name__ == "__main__":
    uvicorn.run(app)
