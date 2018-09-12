import socket, time
import threading
from common.common import *
from common.message import *

recvdatalen = 1024
SEPARATOR = '#'

class Client(object):
    def __init__(self, addr, port):
        self._addr = addr
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._socket.connect((self._addr, self._port))
        except socket.error:
            print('Connect server failed.')
        self._message = CMessage()
        self.start()

    def start(self):
        self._recvdatathread = threading.Thread(target=self.recvdata)
        self._recvdatathread.start()

    def join(self):
        self._recvdatathread.join()

    def recvdata(self):
        while True:
            try:
                buff = self._socket.recv(recvdatalen)
                # if buff != b'':
                #     print('Received {}'.format(buff))
                thread = threading.Thread(target=self._message.unpack, args=(buff, self))
                thread.start()
            except Exception:
                print('Lose connection.')
                self._socket.close()
                break

    def processrequestcode(self, reqcode, data):
        #print(time.localtime(time.time()))
        print('Received: ({0}, {1})'.format(actioncode(reqcode).name, data))

    def registure(self, name, pwd):
        buff = self._message.pack(requestcode.account, actioncode.registure, name + ' ' + pwd + SEPARATOR)
        if buff:
            self.senddata(buff)

    def updatepwd(self, name, pwd):
        buff = self._message.pack(requestcode.account, actioncode.updatepwd, name + ' ' + pwd + SEPARATOR)
        if buff:
            self.senddata(buff)

    def login(self, name, pwd):
        buff = self._message.pack(requestcode.account, actioncode.login, name + ' ' + pwd + SEPARATOR)
        if buff:
            self.senddata(buff)

    def logout(self):
        buff = self._message.pack(requestcode.account, actioncode.logout, '' + SEPARATOR)
        if buff:
            self.senddata(buff)

    def senddata(self, buff):
        try:
            self._socket.send(buff)
        except socket.error:
            print('Send data to server failed')