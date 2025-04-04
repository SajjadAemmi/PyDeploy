import os
from time import sleep
from datetime import datetime
from celery import Celery


app = Celery("tasks", 
             broker="redis://localhost:6379", 
             backend="redis://localhost:6379")


@app.task
def hello_world():
    return "Hello World!"

@app.task
def dummy_task():
    os.makedirs("./tmp/celery", exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%s")
    with open(f"./tmp/celery/task-{now}.txt", "w") as f:
        f.write("سلام بر کفار تمرین‌ها")


@app.task
def dummy_task_2(name="Sajjad"):
    sleep(10)
    return f"Hello {name}!"
