import os
from time import sleep
from datetime import datetime
from celery import Celery


app = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')

@app.task
def add(x, y):
    print("add function")
    return x + y


# Define a simple task
@app.task
def hello_world():
    return 'Hello, World!'

@app.task
def dummy_task():
    folder = "./tmp/celery"
    os.makedirs(folder, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%s")
    with open(f"{folder}/task-{now}.txt", "w") as f:
        f.write("hello!")


@app.task
def dummy_task_2(name='Bob') -> str:
    sleep(5)
    return f'Hello {name}!'


@app.task
def dummy_task_3() -> str:
    return open('./tmp/celery/x.txt', 'w')
