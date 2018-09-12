from Server.tables import *

controllerdict = dict()
usercount = 0

class basecontroller(object):
    def __init__(self):
        pass

    def processrequest(self, actcode, data):
        pass

    def enum_to_bytes(self, retcode):
        return bytes('{}'.format(retcode.value), encoding='utf-8')

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
            user = User(user_index=0, user_name=name, user_pwd=pwd, user_level=0, user_now_exp=0)
            retcode = await user.save()
            return actcode, self.enum_to_bytes(retcode)
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    async def updatepwd(self, actcode, data):
        try:
            name, pwd = data.split()
            user = User(user_index=0, user_name=name, user_pwd=pwd)
            retcode = await user.update()
            return actcode, self.enum_to_bytes(retcode)
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    async def login(self, actcode, data):
        try:
            name, pwd = data.split()
            user = User(user_index=0, user_name=name, user_pwd=pwd)
            retcode = await user.verify(name, pwd)
            return actcode, self.enum_to_bytes(retcode)
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    async def clear(self, data):
        await User.clear()

class roomcontroller(basecontroller):

    def __init__(self, reqcode = requestcode.room):
        self._requestcode = reqcode
        self._actiondict = dict()
        self._actiondict[actioncode.create] = self.create
        super(roomcontroller, self).__init__()
        controllerdict[self._requestcode] = self

    async def processrequest(self, actcode, data):
        return await self._actiondict[actcode](actcode, data)

    async def create(self, actcode, data):
        pass