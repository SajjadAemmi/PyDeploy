from celery_app import add
add.delay(4, 4)

add.apply_async(args=(4, 4), countdown=60)