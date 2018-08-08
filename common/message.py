import struct
import sys

leni = struct.calcsize('i')

class SMessage(object):

    def pack(self, requestcode, data):
        pformat = 'i i {}s'.format(len(data))
        buff = struct.pack(pformat, (leni + len(data)), requestcode, bytes(data))
        return buff

#(len:requestcode:actioncode:data)
    def unpack(self, buff, server, client):
        self._index = 0
        self._bufflen = len(buff)
        if self._bufflen < 4:
            return
        while True:
            try:
                l, = struct.unpack('i', buff[0:leni])
                self._index = leni + l
                reqcode, = struct.unpack('i', buff[leni:leni*2])
                actcode, = struct.unpack('i', buff[leni*2:leni*3])
                upkformat = '{}s'.format(l - leni*2)
                data, = struct.unpack(upkformat, buff[leni*3:self._index])
                print(reqcode, actcode, data)
                buff = buff[self._index:]
            except Exception:
                print('Unpack buffer error.')
                break
            server.processrequest(reqcode, actcode, data, client)

class CMessage(object):

    def pack(self, requestcode, actioncode, data):
        pformat = 'i i i {}s'.format(len(data))
        buff = struct.pack(pformat, leni + leni + len(data), requestcode, actioncode, data)
        return buff

#(len:requestcode:data)
    def unpack(self, buff, client):
        self._index = 0
        self._bufflen = len(buff)
        while True:
            if self._bufflen < 4:
                return
            try:
                l, = struct.unpack('i', buff[0:leni])
                self._index = leni + l
                reqcode, = struct.unpack('i', buff[leni:leni*2])
                upkformat = '{}s'.format(l - leni)
                data, = struct.unpack(upkformat, buff[leni*2:self._index])
                buff = buff[self._index:]
            except Exception:
                # print('Unpack buffer error.')
                break
            client.processrequestcode(reqcode, data)
