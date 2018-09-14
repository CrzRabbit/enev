import asyncio
from Server import *

ADDRESS = '127.0.0.1'
PORT = 20000
BUFFLEN = 2048
SEPARATOR = b'#'

server_processor = server.server(ADDRESS, PORT)

async def async_server(reader, writer):
    while True:
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
        except asyncio.streams.IncompleteReadError as e:
        # don't process data when error, just return
            print('IncompleteReadError')
            return None
        except ConnectionResetError as e:
        # don't process connection error, just return
            print('COnnectionResetError')
            return None

async def init(loop):
    await ORM.create_pool(loop, user='root', password='wang0010', database='gameserverdb')

if __name__ == '__main__':
    global host

    loop = asyncio.get_event_loop()

    #inti controller and create pool
    controller.accountcontroller()
    controller.roomcontroller()
    loop.run_until_complete(init(loop))
    #init server corotine
    server_coro = asyncio.start_server(async_server, ADDRESS, PORT, loop=loop)

    server = loop.run_until_complete(server_coro)
    host = server.sockets[0].getsockname()
    print('Server running on {}...'.format(host))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Server closed.')
        server.close()
        loop.run_until_complete(server.wait_closed())
    finally:
        loop.close()
        print('Loop closed.')