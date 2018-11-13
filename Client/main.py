#!/usr/bin/env python3.5
from Client.client import *
import time

local_addr = '127.0.0.1'
port = 20000
test_amount = 10000

server_addr = '132.232.184.54'

if __name__ == '__main__':

    # for test
    #print(time.localtime(time.time()))
    client = Client(server_addr, port)
    for i in range(0,test_amount):
        client.registure('wangjiangchuan', 'wang0010')
        client.login('wangjiangchuan', 'wang0010')
        client.create_room('testroom1', 'wangjiangchuan', '@', '127.0.0.1', '20001', '0', '0', '1', '1', '6')
        client.list_room()
        client.logout('wangjiangchuan', 'wang0010')
        client.remove_room('4')
        client.updateinfo('1', '1', '100')
        client.update_room('3', 'testroom', 'wangjiangchuan', '@', '127.0.0.1', '20001', '0', '0', '1', '1', '6')
        client.update_room('3', 'testroom', 'wangjiangchuan', '@', '127.0.0.1', '20001', '0', '0', '1', '7', '6')
        time.sleep(0.1)

    client.join()
