# send_task.py
from celery_app import hello_world

# Sending a task to Celery
result = hello_world.delay()

# Getting the result (this might be asynchronous depending on your setup)
print(f'Task result: {result.get(timeout=10)}')
