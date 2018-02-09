import socket
from client import *
from controller import *

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
        print('Server started. Wariting for connecting...')
        while True:
            clientsocket, clientaddr = self._socket.accept()
            c = client(clientsocket, clientaddr, self)
            c.start()
            self._clientsocket.append(c)

    def processrequest(self, requestcode, actioncode, data, client):
        print(controllerdict)
        retrc, retdata = controllerdict[requestcode].processrequest(actioncode, data)
        client.processret(retrc, retdata)

    def remove(self, client):
        self._clientsocket.remove(client)

    def close(self):
        self._socket.close()
        for clientsocket in self._clientsocket:
            clientsocket.close()