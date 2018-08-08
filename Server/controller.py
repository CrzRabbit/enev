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
        super(accountcontroller, self).__init__()
        controllerdict[self._requestcode] = self

    async def processrequest(self, actcode, data):
        return await self._actiondict[actcode](data)

    async def registure(self, data):
        global usercount
        name, pwd = data.split()
        user = User(user_index=usercount, user_name=name, user_pwd=pwd)
        retdata = await user.save()
        usercount += 1
        return self._requestcode, retdata

    async def updatepwd(self, data):
        name, pwd = data.split()
        user = User(user_index=0, user_name= name, user_pwd=pwd)
        retdata = await user.update()
        return self._requestcode, retdata

    async def clear(self, data):
        await User.clear()