import struct
from common.common import *

SEPARATOR_LEN = 1

leni = struct.calcsize('i')
class Message(object):
    def __init__(self, requestcode=requestcode.default, actioncode=actioncode.default, data=''):
        self._requestcode = requestcode
        self._actioncode = actioncode
        self._data= data

    def get(self):
        return self._requestcode, self._actioncode, self._data

#message for server
class SMessage(object):
    def pack(self, requestcode, data):
        pformat = None
        try:
            pformat = 'i i {}s'.format(len(data))
            # buff = struct.pack(pformat, (leni + len(data)), requestcode.value, bytes(data, encoding='utf-8'))
            buff = struct.pack(pformat, (leni + len(data)), requestcode.value, data)
            return buff
        except struct.error:
            #print('Pack Message Error:\n    format: {0}\n    len: {1}\n    '
            #      'requestcode: {2}\n    data: {3}'.format(pformat, leni + len(data), requestcode, data))
            return None

#(len:requestcode:actioncode:data)
    async def unpack(self, buff, server):
        self._index = 0
        self._bufflen = len(buff)
        ret = []
        if self._bufflen < 4:
            return None
        while True:
            try:
                l, = struct.unpack('i', buff[0:leni])
                self._index = leni + l
                reqcode, = struct.unpack('i', buff[leni:leni*2])
                actcode, = struct.unpack('i', buff[leni*2:leni*3])
                #we should abandon separator: '#'
                upkformat = '{}s'.format(l - SEPARATOR_LEN - leni*2)
                data, = struct.unpack(upkformat, buff[leni*3:self._index - SEPARATOR_LEN])
                #print('({0}, {1}, {2})'.format(requestcode(reqcode).name, actioncode(actcode).name, data))
                ret.append(Message(requestcode(reqcode), actioncode(actcode), data))
                buff = buff[self._index:]
            except Exception:
                #print('Unpack buffer error.')
                #ret.clear()
                break
        return await server.processrequest(ret)

#message for client
class CMessage(object):
    def pack(self, requestcode, actioncode, data):
        pformat = None
        try:
            pformat = 'i i i {}s'.format(len(data))
            #print(requestcode, actioncode, data)
            return struct.pack(pformat, leni + leni + len(data), requestcode.value, actioncode.value, bytes(data, encoding='utf-8'))
        except struct.error as e:
            # print('Pack Message Error:\n    format: {0}\n    len: {1}\n    requescode: {2}\n    '
            #       'actioncode: {3}\n    data: {4}'.format(pformat, leni + leni + len(data), requestcode, actioncode, data))
            return None

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
                #print('Unpack buffer error.')
                break
            client.processrequestcode(reqcode, data)
