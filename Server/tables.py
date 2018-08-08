from Server.ORM import *
import time, uuid

def next_id():
    return '{0:0>15}{1}000'.format(int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'users'

    # id = StringField(primary_key=True, default=next_id, ddl='varchar(50')
    # email = StringField(ddl='varchar(50)')
    # passwd = StringField(ddl='varchar(50')
    # admin = BooleanField()
    # name = StringField(ddl='varchar(50)')
    # image = StringField(ddl='varchar(500)')
    # created_at = FloatField(default=time.time)
    user_index = IntegerField(primary_key=True)
    user_name = StringField(ddl='varchar(20)')
    user_pwd = StringField(ddl='varchar(20)')
