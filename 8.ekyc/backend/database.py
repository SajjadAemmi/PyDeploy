from mongoengine import connect, Document, StringField, EmailField, IntField


connect(host="mongodb://localhost:27017/ekyc")


class User(Document):
    email = EmailField(required=True, unique=True)
    hashed_password = StringField(required=True)
    level = IntField(required=True)
