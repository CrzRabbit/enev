import asyncio
from Server import *

ADDRESS = '127.0.0.1'
PORT = 20000
server_pro = server.server(ADDRESS, PORT)

async def async_server(reader, writer):
    while True:
        await writer.drain()
        data = await reader.readline()
        client = writer.get_extra_info('peername')
        if data != b'':
            print('Received from {0}: {1}'.format(client, data))
            retrc, retdata = await server_pro.processdata(data)
            # writer.writelines(' '.join((''.format(retrc), retdata)))
            response_data = await server_pro.processretdata(retrc, retdata)
            writer.write(response_data)
        await writer.drain()

async def init(loop):
    await ORM.create_pool(loop, user='root', password='wang0010', database='gameserverdb')

if __name__ == '__main__':
    global host

    loop = asyncio.get_event_loop()

    controller.accountcontroller()
    loop.run_until_complete(init(loop))

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
