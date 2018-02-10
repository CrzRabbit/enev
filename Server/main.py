from server import *
from controller import *

addr = '127.0.0.1'
port = 20000

if __name__ == '__main__':

    accountcontroller()
    logiocontroller()

    print('Start server...')

    server = server(addr, port)

    try:
        server.serverstart()
    finally:
        server.close()
