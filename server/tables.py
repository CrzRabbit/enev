from server.ORM import *
import time, uuid

def next_id():
    return '{0:0>15}{1}000'.format(int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'users'
    __id__ = (('user_index',), ('user_name', 'user_pwd'))
    __create__ = ('''CREATE TABLE IF NOT EXISTS `users` (
  `user_index` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(20) NOT NULL,
  `user_pwd` varchar(45) NOT NULL,
  `user_level` bigint(20) NOT NULL DEFAULT '0',
  `user_cur_exp` bigint(20) NOT NULL DEFAULT '0',
  `user_online` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_index`),
  UNIQUE KEY `user_name_UNIQUE` (`user_name`),
  UNIQUE KEY `user_index_UNIQUE` (`user_index`),
  UNIQUE KEY `user_pwd_UNIQUE` (`user_pwd`)
);''')

    user_index = IntegerField(primary_key=True)
    user_name = StringField(ddl='varchar(20)')
    user_pwd = StringField(ddl='varchar(20)')
    user_level = IntegerField()
    user_cur_exp = IntegerField()
    user_online = BooleanField()

class Room(Model):
    __table__ = 'rooms'
    __id__ = (('room_index',), ('room_ip', 'room_port'), ('room_owner',))
    __create__ = ('''CREATE TABLE IF NOT EXISTS `rooms` (
  `room_index` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `room_name` varchar(40) NOT NULL,
  `room_owner` varchar(45) NOT NULL,
  `room_pwd` varchar(6) DEFAULT NULL,
  `room_ip` varchar(20) NOT NULL,
  `room_port` bigint(20) NOT NULL,
  `room_scene` varchar(40) NOT NULL,
  `room_state` int(11) NOT NULL,
  `room_level` bigint(20) NOT NULL DEFAULT '0',
  `room_cur_count` int(11) NOT NULL DEFAULT '0',
  `room_max_count` int(11) NOT NULL,
  PRIMARY KEY (`room_index`)
);''')

    room_index = StringField(primary_key=True)
    room_name = StringField(ddl='varchar(40)')
    room_owner = StringField(ddl='varchar(20)')
    room_pwd = StringField(ddl='varchar(6)')
    room_ip = StringField(ddl='varchar(20)')
    room_port = IntegerField()
    room_scene = StringField(ddl='varchar(40')
    #state ready or playing
    room_state = BooleanField()
    room_level = IntegerField()
    room_cur_count = IntegerField()
    room_max_count = IntegerField()