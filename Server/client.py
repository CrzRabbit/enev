import threading

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
        bytes = self._message.pack(0, 'Welcome~')
        self._socket.send(bytes)
        while True:
            try:
                buff = self._socket.recv(recvdatalen)
            except Exception:
                self.close()
                break
            thread = threading.Thread(target=self._message.unpack, args=(buff, self._server, self))
            thread.start()
            #requestcode, actioncode, data = self._message.unpack(buff)
            #self._server.processrequest(requestcode, actioncode, data)

    def processret(self, requestcode, data):
        buff = self._message.pack(requestcode, data)
        self._socket.send(buff)

    def close(self):
        self._socket.close()
        self._server.remove(self)