from Server.controller import *
from common.message import *

class server(object):

    def __init__(self, addr, port):
        self._message = SMessage()
        self._controllerdict = controllerdict

    async def processdata(self, data):
        return await self._message.unpack(data, self)

    async def processretdata(self, reqcode, data):
        return self._message.pack(reqcode, data)

    async def processrequest(self, ret):
        buff = b''
        for message in ret:
            reqcode, actcode, data = message.get()
            retrc, retdata = await controllerdict[requestcode(reqcode)].processrequest(actioncode(actcode), data)
            buff += await self.processretdata(retrc, retdata)
        return buff

    async def clear(self):
        await controllerdict[requestcode.account].processrequest(actioncode.clear, '')