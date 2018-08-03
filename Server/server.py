import socket
from Server.client import *
from Server.controller import *
from common.common import *

class server(object):

    def __init__(self, addr, port):
        self._addr = addr
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._addr, self._port))
        self._clientsocket = []

    def __str__(self):
        return '{0}:{1}'.format(self._addr, self._port)

    def serverstart(self):
        self._socket.listen(0)
        print('Server started. Waiting for connecting...')
        while True:
            clientsocket, clientaddr = self._socket.accept()
            print('{} connected.'.format(clientaddr))
            cnt = client(clientsocket, clientaddr, self)
            self._clientsocket.append(cnt)

    def processrequest(self, reqcode, actcode, data, client):
        retrc, retdata = controllerdict[requestcode(reqcode)].processrequest(actioncode(actcode), data)
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