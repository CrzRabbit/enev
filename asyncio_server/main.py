#!/usr/bin/env python3.5
import asyncio
from Server import *
from debug.log import *
from common.common import *

LOCAL_ADDRESS = '127.0.0.1'
SERVER_ADDRESS = '172.27.0.9'
PORT = 20000
BUFFLEN = 2048
SEPARATOR = b'#'

server_processor = server.server()

async def async_server(reader, writer):
    while True:
        server_processor.save_client(writer)
        server_processor.set_currentclient(writer)
        await writer.drain()
        #client_data = await reader.read(BUFFLEN)
        try:
            client_data = await reader.readuntil(SEPARATOR)
            #client_info = writer.get_extra_info('peername')
            if client_data != b'':
                #print('Received from {0}: {1}'.format(client_info, client_data))
                response_data = await server_processor.processdata(client_data)
                if response_data:
                    writer.write(response_data)
                    await writer.drain()
                else:
                    loge(logcf.message, "[ERROR] get wrong data from client: {}".format(client_data))
        except asyncio.streams.IncompleteReadError as e:
        # don't process data when error, just return
            logi(logcf.base, 'IncompleteReadError')
            await server_processor.remove_client(writer)
            return None
        except ConnectionResetError as e:
        # don't process connection error, just return
            logi(logcf.base, 'ConnectionResetError')
            await server_processor.remove_client(writer)
            return None

async def send_to_client(writer, data):
    if data:
        writer.write(data)
        await writer.drain()

async def init(accountctrl, roomctrl, loop):
    # connect database
    await ORM.create_pool(loop, user='root', password='wang0010', database='gameserverdb')
    # make all users offline
    await accountctrl.offline_all(actioncode.offline_all, '')
    # clear all rooms
    await roomctrl.remove_all(actioncode.remove_all, '')

if __name__ == '__main__':

    global host
    loop = asyncio.get_event_loop()

    #init controller and create pool
    accountctrl =  controller.accountcontroller()
    roomctrl = controller.roomcontroller()
    loop.run_until_complete(init(accountctrl, roomctrl, loop))

    #init server corotine
    server_coro = asyncio.start_server(async_server, SERVER_ADDRESS, PORT, loop=loop)

    server = loop.run_until_complete(server_coro)
    host = server.sockets[0].getsockname()
    logi(logcf.base, 'Server running on {}...'.format(host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logi(logcf.base, 'Server closed.')
        server.close()
        loop.run_until_complete(server.wait_closed())
    finally:
        loop.close()
        logi(logcf.base, 'Loop closed.')