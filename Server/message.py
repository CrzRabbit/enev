import struct
import sys

leni = struct.calcsize('i')

class SMessage(object):

    def pack(self, requestcode, data):
        pformat = 'i i {0}s'.format(len(data))
        buff = struct.pack(pformat, (leni + len(data)), requestcode, data)
        return buff

#(len:requestcode:actioncode:data)
    def unpack(self, buff, server, client):
        l, = struct.unpack('i', buff[0:leni])
        requestcode, = struct.unpack('i', buff[leni:leni*2])
        actioncode, = struct.unpack('i', buff[leni*2:leni*3])
        upkformat = '{0}s'.format(l - leni*2)
        data, = struct.unpack(upkformat, buff[leni*3:])
        server.processrequest(requestcode, actioncode, data, client)

class CMessage(object):

    def pack(self, requestcode, actioncode, data):
        pformat = 'i i i {0}s'.format(len(data))
        buff = struct.pack(pformat, leni + leni + len(data), requestcode, actioncode, data)
        return buff

#(len:requestcode:data)
    def unpack(self, buff):
        l, = struct.unpack('i', buff[0:leni])
        requestcode, = struct.unpack('i', buff[leni:leni*2])
        upkformat = '{0}s'.format(l - leni)
        data, = struct.unpack(upkformat, buff[leni*2:])
        return requestcode, data
