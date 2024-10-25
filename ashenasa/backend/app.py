from fastapi import FastAPI, UploadFile, BackgroundTasks
from celery.result import AsyncResult
from .tasks import face_verification, speech_to_text, gesture_recognition


app = FastAPI()


@app.post("/authenticate/face")
async def authenticate_face(file: UploadFile):
    task = face_verification.delay(await file.read())
    return {"task_id": task.id, "status": "processing"}


@app.post("/authenticate/speech")
async def authenticate_speech(file: UploadFile):
    task = speech_to_text.delay(await file.read())
    return {"task_id": task.id, "status": "processing"}


@app.post("/authenticate/gesture")
async def authenticate_gesture(file: UploadFile):
    task = gesture_recognition.delay(await file.read())
    return {"task_id": task.id, "status": "processing"}


@app.get("/task_status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id)
    if result.state == "PENDING":
        return {"status": "pending"}
    elif result.state == "SUCCESS":
        return {"status": "completed", "result": result.result}
    else:
        return {"status": "failed"}
