# eKYC

## How to run

1. Run redis container

```
docker pull redis
docker run --name some-redis -d -p 6379:6379 redis
```

2. Run celery tasks

```
celery -A celery_tasks worker --loglevel=ERROR
```

3. Run mongo container

```
docker pull mongo
docker run --name some-mongo -d -p 27017:27017 mongo
```

4. Run main API

```
fastapi dev app.py
```
