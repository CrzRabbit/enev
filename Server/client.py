import threading
from common.message import *
from common.common import *
import asyncio

recvdatalen = 1024

class client(object):
    def __init__(self, socket, addr, server):
        self._socket = socket
        self._addr = addr
        self._server = server
        self._message = SMessage()
        self._exdatathread = threading.Thread(target=self.start)
        self._exdatathread.start()

    def start(self):
        self.processret(requestcode.default, 'Welcome~')
        while True:
            try:
                buff = self._socket.recv(recvdatalen)
            except Exception:
                self.close()
                break
            thread = threading.Thread(target=self._message.unpack, args=(buff, self._server, self))
            thread.start()

    def processret(self, requestcode, data):
        buff = self._message.pack(requestcode, data)
        if buff:
            self._socket.send(buff)

    def close(self):
        self._socket.close()
        self._server.remove(self)