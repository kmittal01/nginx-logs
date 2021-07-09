import datetime
from mongoengine import connect, Document, StringField, BooleanField, DateTimeField, IntField
connect('column', host='mongo', port=27017, username="column", password="password", authentication_source='admin')


class User(Document):
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=datetime.datetime.utcnow())
    email = StringField(required=True, max_length=100, unique=True)
    first_name = StringField(max_length=200)
    last_name = StringField(max_length=200)
    hashed_password = StringField()
    is_active = BooleanField(required=True, default=True)
    is_superuser = BooleanField(required=True, default=False)
    username = StringField(max_length=200, required=False)
    profile_pic = StringField(max_length=300)
