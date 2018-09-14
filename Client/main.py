from Client.client import *
import time

addr = '127.0.0.1'
port = 20000
test_amount = 1

if __name__ == '__main__':

    client = Client(addr, port)

    #print(time.localtime(time.time()))
    for i in range(0,test_amount):
        client.registure('wangjiangchuan', 'wang0010')
        client.login('wangjiangchuan', 'wang0010')
        client.create_room('wangjiangchuan', '101686', 'test_scene', '0', '1', '1', '6')
        time.sleep(0.5)

    client.join()
