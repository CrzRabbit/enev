from DAO import *

controllerdict = dict()

class basecontroller(object):
    def __init__(self):
        # self._requestcode = requestcode.default
        self._DAO = DAO()

    def processrequest(self, actcode, data):
        pass

class accountcontroller(basecontroller):
    def __init__(self, reqcode = requestcode.account):
        self._requestcode = reqcode
        super(accountcontroller, self).__init__()
        controllerdict[self._requestcode] = self
        # controllerdict.__setitem__(self._requestcode, self)

    def processrequest(self, actcode, data):
        ret = None
        if actcode == actioncode.registure:
            ret = self.registure(data)
        elif actcode == actioncode.updatepwd:
            ret = self.updatepwd(data)
        return ret

    def registure(self, data):
        name, pwd = data.split()
        sql = 'INSERT INTO user (user_name, user_pwd) VALUES (%s, %s)'
        return self._DAO.insert(sql, name, pwd)

    def updatepwd(self, data):
        name, pwd = data.split()
        sql = 'UPDATE user SET user_pwd = %s WHERE user_name = %s'
        return self._DAO.update(sql, pwd, name)

    def getusers(self):
        sql = 'SELECT * FROM user;'
        return self._DAO.select(sql)

    def deleteuser(self, data):
        name = data
        sql = 'DELETE FROM user WHERE user_name = %s'
        return self._DAO.delete(sql, name)

# data = 'wangjiangchuan wang0010'
# data1 = 'wangjiangchuan wjc'
# accountcontroller().registure(data)
# accountcontroller().updatepwd(data1)
# accountcontroller().getusers()
# data3 = 'wangjiangchuan'
# accountcontroller().deleteuser(data3)

class logiocontroller(basecontroller):
    def __init__(self, reqcode = requestcode.logio):
        self._requestcode = reqcode
        super(logiocontroller, self).__init__()
        controllerdict[self._requestcode] = self
        # controllerdict.__setitem__(self._requestcode, self)

    def processrequest(self, actcode, data):
        ret = None
        if actcode == actioncode.login:
            ret = self.login()
        elif actcode == actioncode.logout:
            ret = self.logout()
        return ret

    def login(self):
        return self._requestcode, 'OK'

    def logout(self):
        return self._requestcode, 'OK'