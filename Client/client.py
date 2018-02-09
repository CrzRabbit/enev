import socket
from message import *
from common import *

recvdatalen = 1024

class Client(object):
    def __init__(self, addr, port):
        self._addr = addr
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._addr, self._port))
        self._message = CMessage()

    def start(self):
        while True:
            buff = self._socket.recv(recvdatalen)
            print(self._message.unpack(buff))

    def registure(self, name, pwd):
        buff = self._message.pack(requestcode.account, actioncode.registure, name + ' ' + pwd)
        self._socket.send(buff)

