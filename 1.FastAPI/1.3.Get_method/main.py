from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/salam")
def test_1():
    return "علیک سلام"


@app.get("/salam/{name}")
def read_item(name: str):
    return "علیک سلام" + " " + name + " جان"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
