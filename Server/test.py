from Server.ORM import *
import asyncio


def init(loop, **kwargs):
    await create_pool(loop, **kwargs)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(init(loop, user='root', password='wang0010', database='gameserverdb'))
    loop.run_forever()