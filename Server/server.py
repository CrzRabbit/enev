from Server.controller import *
from common.message import *
#from asyncio_server.main import *

class server(object):

    def __init__(self):
        self._message = SMessage()
        self._controllerdict = controllerdict
        self._clients = list()

    async def processdata(self, data):
        return await self._message.unpack(data, self)

    async def processretdata(self, actcode, data):
        return self._message.pack(actcode, data)

    async def processrequest(self, ret):
        buff = b''
        for message in ret:
            reqcode, actcode, data = message.get()
            retrc, retdata = await controllerdict[requestcode(reqcode)].processrequest(actioncode(actcode), data)
            if reqcode == requestcode.room and (actcode == actioncode.create or actcode == actioncode.update):
                retrc, retdata = await  controllerdict[requestcode(reqcode)].processrequest(actioncode(actioncode.list), '')
                data = b''
                data += await self.processretdata(retrc, retdata)
                await self.send_all(data)
            buff += await self.processretdata(retrc, retdata)
        return buff

    async def clear(self):
        await controllerdict[requestcode.account].processrequest(actioncode.clear, '')

    def save_client(self, client):
        self._clients.append(client)

    def remove_client(self, client):
        self._clients.remove(client)

    async def send_all(self, data):
        for client in self._clients:
            client.write(data)
            await client.drain()
