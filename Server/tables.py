from Server.ORM import *
import time, uuid

def next_id():
    return '{0:0>15}{1}000'.format(int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'users'

    user_index = IntegerField(primary_key=True)
    user_name = StringField(ddl='varchar(20)')
    user_pwd = StringField(ddl='varchar(20)')
