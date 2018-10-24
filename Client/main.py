from Client.client import *
import time

addr = '127.0.0.1'
port = 20000
test_amount = 1

if __name__ == '__main__':

    # for test
    #print(time.localtime(time.time()))
    client = Client(addr, port)
    for i in range(0,test_amount):
        # client.registure('wangjiangchuan', 'wang0010')
        # client.login('wangjiangchuan', 'wang0010')
        # client.create_room('testroom1', 'wangjiangchuan1', '@', '127.0.0.1', '20001', '0', '0', '1', '1', '6')
        # client.list_room()
        # client.logout('wangjiangchuan', 'wang0010')
        # client.remove_room('4')
        # client.updateinfo('1', '1', '100')
        # client.update_room('3', 'testroom', 'wangjiangchuan', '@', '127.0.0.1', '20001', '0', '0', '1', '1', '6')
        # client.update_room('3', 'testroom', 'wangjiangchuan', '@', '127.0.0.1', '20001', '0', '0', '1', '7', '6')
        time.sleep(0.5)

    client.join()
