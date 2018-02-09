from client import *

addr = '127.0.0.1'
port = 20000

if __name__ == '__main__':
    client = Client(addr, port)
    client.registure('wangjiangchuan', 'wang0010')
    client.start()