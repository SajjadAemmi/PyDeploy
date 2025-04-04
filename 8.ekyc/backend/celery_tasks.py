import time
import random
import requests
from celery import Celery



celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379'
)


@celery_app.task
def face_task(face_data: bytes):
    time.sleep(15)
    result = random.choice([True, False])
    return {
        "status": "completed",
        "result": result
    }


@celery_app.task
def speech_task(speech_data: bytes):
    time.sleep(5)
    result = random.choice([True, False])
    return {
        "status": "completed",
        "result": result
    }


@celery_app.task
def gesture_task(gesture_data: bytes):
    files=[
        ('file',('thumbs_down.jpg',
                 gesture_data,
                 'image/jpeg'))
    ]
    response = requests.post("http://127.0.0.1:8080/auth/gesture", files=files)
    result = response.json()
    return {
        "status": "completed",
        "result": result
    }


@celery_app.task
def national_card_task(image: bytes):
    url = "https://partai.gw.isahab.ir/nationalCardProcessing/v1/file"

    payload = {'nationalCode': 'true',
        'name': 'true',
        'familyName': 'true',
        'fatherName': 'true',
        'birthday': 'true',
        'expirationDate': 'true',
        'imagePath': 'true',
        'base64': '0',
        'checksum': 'true',
        'id': 'true',
        'location': 'true',
        'face': 'true',
        'serial': '1',
        'postalCode': '1'
    }
    files=[
        ('file',('photo_1403-09-24 18.50.42.jpeg',image,'image/jpeg'))
    ]
    headers = {
        'gateway-token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzeXN0ZW0iOiJzYWhhYiIsImNyZWF0ZVRpbWUiOiIxNDAzMDkyNDIwNDkyNDMxNSIsInVuaXF1ZUZpZWxkcyI6eyJ1c2VybmFtZSI6IjA1OGZkNjlmLWMwMjQtNGQ2My05Nzg1LTMzNGY3MTUyZjQ2OSJ9LCJkYXRhIjp7InNlcnZpY2VJRCI6ImY1MTdlNDhiLWI2OTUtNDQ1NS05NDZmLTQ3MGJkNzNlN2E1NSIsInJhbmRvbVRleHQiOiJmS1JMSCJ9LCJncm91cE5hbWUiOiIyZWQ1YzNkNGYyZGRjZWNlMmJhMTMwY2U2ZWRmNmUxNyJ9.OXpuvRwAWd_Z_VDrPPlNpFuLVcRUiDdqaj-lGayi5rw"
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    result = response.json()
    return {
        "status": "completed",
        "result": result
    }
