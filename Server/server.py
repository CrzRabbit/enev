import socket
from Server.controller import *
from common.common import *
from common.message import *
import asyncio

class server(object):

    def __init__(self, addr, port):
        self._message = SMessage()
        self._controllerdict = controllerdict

    async def processdata(self, data):
        return await self._message.unpack(data, self)

    async def processretdata(self, reqcode, data):
        return self._message.pack(reqcode, data)

    async def processrequest(self, reqcode, actcode, data):
        retrc, retdata = await controllerdict[requestcode(reqcode)].processrequest(actioncode(actcode), data)
        return retrc, retdata

    def remove(self, client):
        try:
            self._clientsocket.remove(client)
        except Exception:
            print('Close client error.')

    def close(self):
        self._socket.close()
        for clientsocket in self._clientsocket:
            clientsocket.close()