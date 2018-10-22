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

    #infotype： 0(user_pwd) 1(user_level) 2(usr_cur_exp)
    async def updateinfo(self, actcode, data):
        try:
            index_bytes, infotype_bytes, info = data.split()
            index = int(index_bytes)
            infotype = int(infotype_bytes)
            user = User(user_index=index)
            retcode, user = await user.verify(0, index)
            if infotype == 0:
                user.user_pwd = info
            elif infotype == 1:
                user.user_level = int(info)
            elif infotype == 2:
                user.usr_cur_exp = int(info)
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
                user.user_online = 0
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

    async def clear(self, data):
        await User.clear()

class roomcontroller(basecontroller):

    def __init__(self, reqcode = requestcode.room):
        self._requestcode = reqcode
        self._actiondict = dict()
        self._actiondict[actioncode.create] = self.create
        self._actiondict[actioncode.list] = self.list
        self._actiondict[actioncode.update] = self.update
        self._actiondict[actioncode.remove] = self.remove
        super(roomcontroller, self).__init__()
        controllerdict[self._requestcode] = self

    async def processrequest(self, actcode, data):
        return await self._actiondict[actcode](actcode, data)

    async def create(self, actcode, data):
        try:
            name, owner, pwd, ip, port, scene, state, level, now_count, max_count = data.split()
            if pwd == b'@':
                pwd = ''
            room = Room(room_index=0, room_name=name, room_owner=owner, room_pwd=pwd, room_ip=ip, room_port=port, room_scene=scene, room_state=bool(state), room_level=int(level)
                        , room_cur_count=int(now_count), room_max_count=int(max_count))
            retcode = await room.save()
            if retcode == returncode.success:
                retcode, room = await room.verify(1, ip, port)
                room_data = self.enum_to_bytes(retcode)
                if room.room_pwd == '':
                    room.room_pwd = '@'
                room_data += bytes('|{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}'
                                    .format(room.room_index, room.room_name, room.room_owner, room.room_pwd, room.room_ip,
                                            room.room_port, room.room_scene, room.room_state, room.room_level,
                                            room.room_cur_count, room.room_max_count), encoding='utf-8')
                return actcode, room_data
            return actcode, self.enum_to_bytes(retcode)
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    async def list(self, actcode, data):
        try:
            retcode, rooms = await Room.findAll()
            rooms_data = self.enum_to_bytes(retcode)
            for room in rooms:
                if room.room_pwd == '':
                    room.room_pwd = '@'
                rooms_data += bytes('|{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}'
                                    .format(room.room_index, room.room_name, room.room_owner, room.room_pwd, room.room_ip,
                                            room.room_port, room.room_scene, room.room_state, room.room_level,
                                            room.room_cur_count, room.room_max_count), encoding='utf-8')
            return actcode, rooms_data
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    async def update(self, actcode, data):
        try:
            index, name, owner, pwd, ip, port, scene, state, level, now_count, max_count = data.split()
            if pwd == b'@':
                pwd = ''
            room = Room(room_index=index, room_name=name, room_owner=owner, room_pwd=pwd, room_ip=ip, room_port=port,
                        room_scene=scene, room_state=bool(state), room_level=int(level)
                        , room_cur_count=int(now_count), room_max_count=int(max_count))
            retcode = await room.update()
            return actcode, self.enum_to_bytes(retcode)
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    async def remove(self, actcode, data):
        try:
            index = data
            room = Room(room_index=index)
            retcode = await room.remove()
            return actcode, self.enum_to_bytes(retcode)
        except ValueError as e:
            return actcode, self.enum_to_bytes(returncode.fail)

    async def join(self, actcode, data):
        pass