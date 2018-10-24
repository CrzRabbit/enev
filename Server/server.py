from Server.controller import *
from common.message import *

class server(object):

    def __init__(self):
        self._message = SMessage()
        self._controllerdict = controllerdict
        #just stream writers for send data to client
        self._clients = list()
        self._currentclient = None
        self._users = dict()

    async def processdata(self, data):
        return await self._message.unpack(data, self)

    async def processretdata(self, actcode, data):
        return self._message.pack(actcode, data)

    async def processrequest(self, ret):
        buff = b''
        for message in ret:
            reqcode, actcode, data = message.get()
            retrc, retdata = await controllerdict[requestcode(reqcode)].processrequest(actioncode(actcode), data)
            if reqcode == requestcode.room and (actcode == actioncode.create or actcode == actioncode.update or actcode == actioncode.remove):
                retrc1, retdata1 = await controllerdict[requestcode(reqcode)].processrequest(actioncode(actioncode.list), '')
                rooms_data = b''
                rooms_data += await self.processretdata(retrc1, retdata1)
                await self.send_all(rooms_data)
            if reqcode == requestcode.account and actcode == actioncode.login:
                name, pwd = data.split()
                user = User(user_name=name, user_pwd=pwd)
                self._users[self._currentclient] = user
            buff += await self.processretdata(retrc, retdata)
        return buff

    def save_client(self, client):
        if not self._clients.__contains__(client):
            self._clients.append(client)

    async def remove_client(self, client):
        self._clients.remove(client)
        try:
            user = self._users[client]
            await controllerdict[requestcode.account].processrequest(actioncode.logout, user.user_name + b' ' + user.user_pwd)
        except KeyError as e:
            pass

    def set_currentclient(self, client):
        self._currentclient = client

    async def send_all(self, data):
        for client in self._clients:
            #if client != self._currentclient:
            client.write(data)
            await client.drain()

    async def clear(self):
        await controllerdict[requestcode.account].processrequest(actioncode.clear, '')
