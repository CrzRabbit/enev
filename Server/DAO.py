#import mysql.connector
from common.common import *
from Server.ORM import *
from Server.main import loop

connconfig = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': 'wang0010',
    'database': 'gameserverdb',
}

class DAO(object):
    _instance = None
    def __new__(cls, loop, *args, **kwargs):
        if not cls._instance:
            create_pool(loop, **kwargs)
        return cls._instance

    # def __new__(cls, *args, **kw):
    #     if not cls._instance:
    #         cls._instance = super(DAO, cls).__new__(cls, *args, **kw)
    #         cls._instance.connect()
    #     return cls._instance
    #
    # def connect(self):
    #     self._conn = mysql.connector.connect(**connconfig)
    #     self._cursor = self._conn.cursor()
    #
    # def insert(self, sql, *args):
    #     # sqltmp = 'SELECT * FROM user WHERE  user_name = %s'
    #     # paramtmp = []
    #     # paramtmp.append(args[0])
    #     # if(None != self._cursor.execute(sqltmp, paramtmp, multi=True)):
    #     #      return None
    #     #print sql
    #     params = []
    #     for param in args:
    #         params.append(param)
    #     try:
    #         ret = self._cursor.execute(sql, params)
    #         self._conn.commit()
    #     except Exception:
    #         return requestcode.account, 'ERROR'
    #     return requestcode.account, 'OK'
    #
    # def update(self, sql, *args):
    #     params = []
    #     for param in args:
    #         params.append(param)
    #     ret = self._cursor.execute(sql, params)
    #     self._conn.commit()
    #     return requestcode.account, 'OK'
    #
    # def delete(self, sql, *args):
    #     params = []
    #     params.append(args[0])
    #     ret = self._cursor.execute(sql, params)
    #     self._conn.commit()
    #     return requestcode.account, 'OK'
    #
    # def select(self, sql, *args):
    #     params = []
    #     for param in args:
    #         params.append(param)
    #     self._cursor.execute(sql, params, multi=True)
    #     if self._cursor.fetchone():
    #         return requestcode.logio, 'OK'
    #     else:
    #         return requestcode.logio, 'ERROR'

