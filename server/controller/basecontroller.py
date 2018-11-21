
controllerdict = dict()
usercount = 0

class basecontroller(object):
    def __init__(self):
        pass

    def processrequest(self, actcode, data):
        pass

    def enum_to_bytes(self, retcode):
        return bytes('{}'.format(retcode.value), encoding='utf-8')