import datetime

from peewee import *

db = SqliteDatabase('eventsbase.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField()
    name = CharField()
    surname = CharField()
    phone = CharField(default='not specified')
    status = CharField()
    password = CharField()

class Requests(BaseModel):
    id = AutoField()
    status = CharField(default='В обработке')
    title = CharField()
    date = CharField()
    time = CharField()
    username = CharField()

class Event(BaseModel):
    id = AutoField()
    title = CharField()
    organizer = CharField()
    date = CharField()
    time = CharField()
    space = CharField()
    type = CharField()
    price = IntegerField()
    approval = CharField()
    places = IntegerField()
    members = CharField(default='Пока никого')
    repeat = CharField()
    about = CharField()
    hidden = BooleanField(default=0)


db.create_tables([User, Requests, Event])





