import socket
import threading
from enev.common.common import *
from enev.common.message import *

recvdatalen = 1024

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
                thread = threading.Thread(target=self._message.unpack, args=(buff, self))
                thread.start()
            except Exception:
                print('Lose connection.')
                break

    def processrequestcode(self, reqcode, data):
        print(reqcode, data)

    def registure(self, name, pwd):
        buff = self._message.pack(requestcode.account, actioncode.registure, name + ' ' + pwd)
        self.senddata(buff)

    def updatepwd(self, name, pwd):
        buff = self._message.pack(requestcode.account, actioncode.updatepwd, name + ' ' + pwd)
        self.senddata(buff)

    def login(self):
        buff = self._message.pack(requestcode.logio, actioncode.login, '')
        self.senddata(buff)

    def logout(self):
        buff = self._message.pack(requestcode.logio, actioncode.logout, '')
        self.senddata(buff)

    def senddata(self, buff):
        try:
            self._socket.send(buff)
        except socket.error:
            print('Send data to server failed')