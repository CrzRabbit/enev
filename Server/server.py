import socket
from Server.client import *
from Server.controller import *
from common.common import *
import asyncio
from Server.ORM import *

class server(object):

    def __init__(self, addr, port):
        self._addr = addr
        self._port = port
        #self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self._socket.bind((self._addr, self._port))
        self._clientsocket = []

    def __str__(self):
        return '{0}:{1}'.format(self._addr, self._port)

    @asyncio.coroutine
    def serverstart(self, loop):

        accountcontroller(loop)

        yield from create_pool(loop, user='root', password='wang0010', database='gameserverdb')

        self._socket.listen(0)
        print('Server started. Waiting for connecting...')
        while True:
            clientsocket, clientaddr = self._socket.accept()
            print('{} connected.'.format(clientaddr))
            cnt = client(clientsocket, clientaddr, self)
            self._clientsocket.append(cnt)


    async def processrequest(self, reqcode, actcode, data, client):
        #retrc, retdata = controllerdict[requestcode(reqcode)].processrequest(actioncode(actcode), data)
        #client.processret(retrc, retdata)
        retrc, retdata = await controllerdict[requestcode(reqcode)].processrequest(actioncode(actcode), data)
        client.processret(retrc, retdata)

    def remove(self, client):
        try:
            self._clientsocket.remove(client)
        except Exception:
            print('Close client error.')

    def close(self):
        self._socket.close()
        for clientsocket in self._clientsocket:
            clientsocket.close()