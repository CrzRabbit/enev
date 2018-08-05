from Server.server import *
from Server.controller import *
import asyncio
#from Server.tables import *

addr = '127.0.0.1'
port = 20000
loop = None

#def init(loop):
#    yield from create_pool(loop=loop, host='127.0.0.1', user='root', password='root', database='users')

if __name__ == '__main__':

    #logiocontroller()

    server = server(addr, port)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.serverstart(loop))
    loop.run_forever()

    # print('Start server...')
    #
    # server = server(addr, port)
    #
    # try:
    #     server.serverstart()
    # finally:
    #     server.close()