from server.controller.basecontroller import *
from server.tables import *
from common.common import *

class accountcontroller(basecontroller):
    def __init__(self, reqcode = requestcode.account):
        self._requestcode = reqcode
        self._actiondict = dict()
        self._actiondict[actioncode.registure] = self.registure
        self._actiondict[actioncode.updateinfo] = self.updateinfo
        self._actiondict[actioncode.clear] = self.clear
        self._actiondict[actioncode.login] = self.login
        self._actiondict[actioncode.logout] = self.logout
        super(accountcontroller, self).__init__()
        controllerdict[self._requestcode] = self

    async def processrequest(self, actcode, data):
        return await self._actiondict[actcode](actcode, data)

    async def registure(self, actcode, data):
        try:
            name, pwd = data.split()
            user = User(user_name=name, user_pwd=pwd, user_level=0, user_cur_exp=0)
            retcode = await user.save()
            return actcode, self.enum_to_bytes(retcode)
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    #infotype： 0(user_pwd) 1(user_level) 2(user_cur_exp)
    async def updateinfo(self, actcode, data):
        try:
            index_bytes, infotype_bytes, info = data.split()
            index = int(index_bytes)
            infotype = int(infotype_bytes)
            user = User(user_index=index)
            retcode, user = await user.verify(0, index)
            if user == None:
                raise ValueError
            if infotype == 0:
                user.user_pwd = info
            elif infotype == 1:
                user.user_level = int(info)
            elif infotype == 2:
                user.user_cur_exp = int(info)
            else:
                return actcode, self.enum_to_bytes(returncode.fail)
            retcode = await user.update()
            return actcode, self.enum_to_bytes(retcode)
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    async def login(self, actcode, data):
        try:
            name, pwd = data.split()
            user = User(user_name=name, user_pwd=pwd)
            retcode, user = await user.verify(1, name, pwd)
            if user and user.user_online == 0:
                user.user_online = 1
                await user.update()
                return actcode, self.enum_to_bytes(retcode) + bytes(' {0} {1} {2} {3} {4}'.format(user.user_index, user.user_name, user.user_level, user.user_cur_exp, user.user_online), encoding='utf-8')
            return actcode, self.enum_to_bytes(returncode.fail)
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    async def logout(self, actcode, data):
        try:
            name, pwd = data.split()
            user = User(user_index=0, user_name=name, user_pwd=pwd)
            retcode, user = await user.verify(1, name, pwd)
            if user and user.user_online == 1:
                user.user_online = 0
                retcode = await user.update()
                return actcode, self.enum_to_bytes(retcode)
            return actcode, self.enum_to_bytes(returncode.fail)
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    async def offline_all(self, actcode, data):
        try:
            retcode, users = await User.find_all()
            for user in users:
                user.user_online = 0
                await user.update()
            return actcode, self.enum_to_bytes(returncode.success)
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    async def clear(self, data):
        await User.clear()
