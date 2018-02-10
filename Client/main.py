from client import *

addr = '127.0.0.1'
port = 20000

if __name__ == '__main__':

    client = Client(addr, port)

    client.registure('wangjiangchuan', 'wang0010')
    client.updatepwd('wangjiangchuan', 'Wang0010')
    client.registure('wjc', 'wjc')
    client.updatepwd('wjc', 'Wang0010')
    client.registure('1016864609', '101686@')
    client.login()
    client.logout()

    client.join()