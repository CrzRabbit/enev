import socket
import threading

serveraddr = '127.0.0.1'
port = 20000

def ProcessRequest(clientsocket, clientaddr):
    print('Accepted connection from {0}:{1}'.format(clientsocket, clientaddr))
    clientsocket.send(b'Welcome!')
    while True:
        data = clientsocket.recv(1024)
        if not data or data.decode('utf-8') == 'exit':
            break
        print('{0}:{1} says{2}:'.format(clientsocket, clientaddr, data))
    print('{0}:{1} exit.')

def serverstart():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serversocket.bind((serveraddr, port))

    serversocket.listen(0)

    print('Wariting for connecting...')

    while True:
        clientsocket, clientaddr = serversocket.accept()
        processthread = threading.Thread(target=ProcessRequest, args=(clientsocket, clientaddr))
        processthread.start()

