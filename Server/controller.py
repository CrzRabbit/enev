from common.common import *
from Server.tables import *

controllerdict = dict()

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
        super(accountcontroller, self).__init__()
        controllerdict[self._requestcode] = self

    async def processrequest(self, actcode, data):
        return await self._actiondict[actcode](data)

    async def registure(self, data):
        name, pwd = data.split()
        user = User(user_index=1, user_name=name, user_pwd=pwd)
        retdata = await user.save()
        return self._requestcode, retdata