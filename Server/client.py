import threading
from common.message import *
from common.common import *
import asyncio

recvdatalen = 1024

class client(object):
    def __init__(self, socket, server):
        self._socket = socket
        self._server = server
        self._message = SMessage()

    def processret(self, requestcode, data):
        buff = self._message.pack(requestcode, data)
        if buff:
            self._socket.send(buff)

    def close(self):
        self._socket.close()
        self._server.remove(self)