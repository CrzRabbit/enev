#!/usr/bin/env python3.5
from client.client import *
import time

local_addr = '127.0.0.1'
port = 20000
test_amount = 1

server_addr = '118.24.55.184'

if __name__ == '__main__':

    # for test
    #print(time.localtime(time.time()))
    client = client(local_addr, port)
    for i in range(0,test_amount):
        # client.registure('wangjiangchuan', 'wang0010')
        # client.login('wangjiangchuan', 'wang0010')
        # client.create_room('testroom1', 'wangjiangchuan', '@', '127.0.0.1', '20001', '0', '0', '1', '1', '6')
        # client.list_room()
        # client.logout('wangjiangchuan', 'wang0010')
        # client.remove_room('8934')
        # client.updateinfo('1', '1', '100')
        client.update_room('9145', 'testroom1', 'wangjiangchuan1', '@', '127.0.0.1', '20001', '0', '0', '0', '2', '6')
        # client.update_room('3', 'testroom', 'wangjiangchuan', '@', '127.0.0.1', '20001', '0', '0', '1', '7', '6')
        # time.sleep(0.1)
        pass

    client.join()
