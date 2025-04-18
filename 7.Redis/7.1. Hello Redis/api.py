import time
import json
import requests
from fastapi import FastAPI
import redis


app = FastAPI()
r = redis.Redis(host="localhost", port=6379, decode_responses=True)


@app.get("/women")
def get_women():
    start_time = time.time()
    if r.get("money heist women") is not None:
        women = r.get("money heist women")
    else:
        women = []
        for i in range(1, 29):
            response = requests.get(f"https://project-heist-rahulv07.vercel.app/characters/{i}")
            if response.json()["gender"] == "Female":
                women.append(response.json())
        
        women = json.dumps(women)
        r.set("money heist women", women)
    end_time = time.time()
    print(end_time - start_time)
    return women
