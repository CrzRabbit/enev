import asyncio
from Server import *
from common import *

ADDRESS = '127.0.0.1'
PORT = 20000

async def async_server(reader, writer):
    global host
    global server_pro
    while True:
        await writer.drain()
        data = await reader.readline()
        client = writer.get_extra_info('peername')
        print(client)
        if data != b'':
            print('Received form {0}: {1}'.format(client, data))
            #message.SMessage.unpack(data, server_pro, client)

async def init(loop):
    await ORM.create_pool(loop, user='root', password='wang0010', database='gameserverdb')

if __name__ == '__main__':
    global host
    global server_pro
    server_pro = server.server(ADDRESS, PORT)

    loop = asyncio.get_event_loop()

    controller.accountcontroller(loop)

    server_coro = asyncio.start_server(async_server, ADDRESS, PORT, loop=loop)
    server = loop.run_until_complete(server_coro)
    host = server.sockets[0].getsockname()
    print('Server running on {}'.format(host))
    try:
        loop.run_forever()
    except:
        server.close()
        loop.run_until_complete(server.wait_closed())
    finally:
        loop.close()
