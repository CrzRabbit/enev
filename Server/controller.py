from common.common import *
from Server.tables import *

controllerdict = dict()
usercount = 0

class basecontroller(object):
    def __init__(self):
        pass

    def processrequest(self, actcode, data):
        pass

class accountcontroller(basecontroller):
    def __init__(self, reqcode = requestcode.account):
        self._requestcode = reqcode
        self._actiondict = dict()
        self._actiondict[actioncode.registure] = self.registure
        self._actiondict[actioncode.updatepwd] = self.updatepwd
        self._actiondict[actioncode.clear] = self.clear
        self._actiondict[actioncode.login] = self.login
        super(accountcontroller, self).__init__()
        controllerdict[self._requestcode] = self

    async def processrequest(self, actcode, data):
        return await self._actiondict[actcode](actcode, data)

    async def registure(self, actcode, data):
        try:
            name, pwd = data.split()
            user = User(user_index=0, user_name=name, user_pwd=pwd)
            retcode = await user.save()
            return actcode, bytes('{0}'.format(retcode.value), encoding='utf-8')
        except ValueError as e:
            return actcode, bytes('{0}'.format(returncode.fail.value), encoding='utf-8')

    async def updatepwd(self, actcode, data):
        try:
            name, pwd = data.split()
            user = User(user_index=0, user_name=name, user_pwd=pwd)
            retcode = await user.update()
            return actcode, bytes('{0}'.format(retcode.value), encoding='utf-8')
        except ValueError as e:
            return actcode, bytes('{0}'.format(returncode.fail.value), encoding='utf-8')

    async def login(self, actcode, data):
        try:
            name, pwd = data.split()
            user = User(user_index=0, user_name=name, user_pwd=pwd)
            retcode = await user.find_s(name, pwd)
            return actcode, bytes('{0}'.format(retcode.value), encoding='utf-8')
        except ValueError as e:
            return actcode, bytes('{0}'.format(returncode.fail.value), encoding='utf-8')

    async def clear(self, data):
        await User.clear()