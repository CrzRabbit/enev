from Server.ORM import *
import time, uuid

def next_id():
    return '{0:0>15}{1}000'.format(int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'users'

    user_index = IntegerField(primary_key=True)
    user_name = StringField(ddl='varchar(20)')
    user_pwd = StringField(ddl='varchar(20)')
    user_level = IntegerField()
    user_cur_exp = IntegerField()

class Room(Model):
    __table__ = 'rooms'

    room_index = StringField(primary_key=True)
    room_name = StringField(ddl='varchar(40)')
    room_owner = StringField(ddl='varchar(20)')
    room_pwd = StringField(ddl='varchar(6)')
    room_ip = StringField(ddl='varchar(20)')
    room_port = IntegerField()
    room_scene = StringField(ddl='varchar(40')
    #ready or playing
    room_state = BooleanField()
    room_level = IntegerField()
    room_cur_count = IntegerField()
    room_max_count = IntegerField()