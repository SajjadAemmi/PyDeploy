# app/celery_worker.py

from celery import Celery

celery_app = Celery(
    "biometric_auth",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.task_routes = {
    "tasks.face_verification": {"queue": "face_verification"},
    "tasks.speech_to_text": {"queue": "speech_to_text"},
    "tasks.gesture_recognition": {"queue": "gesture_recognition"},
}
