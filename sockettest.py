# import nnpy
# import time

# s=nnpy.Socket(nnpy.AF_SP,nnpy.REP)
#
#
# s.bind('tcp://127.0.0.1:5555')
#
# # s.setsockopt(option=nnpy.RCVBUF,level=nnpy.SOL_SOCKET,value=1024*1024)
# # s.getsockopt(option=nnpy.RCVBUF,level=nnpy.SOL_SOCKET)
#
# counter=0
# while True:
#     try:
#         res=s.recv(flags=nnpy.DONTWAIT)
#         counter+=1
#     except Exception as e:
#         if not str(e)=='Resource temporarily unavailable':
#             raise(e)
#         from IPython import embed
#         print ("DEBUG NOW 9")
#         embed()
#         raise RuntimeError("stop debug here")
#         time.sleep(1)
#         print(counter)
#         continue
#
#     s.send("ok")
#     # print(res)

from JumpScale import j
def MyMethod(hello):
    import time
    counter=0
    while True:
        time.sleep(1)
        counter+=1
        print("%s:%s"%(hello,counter))

import asyncio
import logging
import aionn

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

counter=0

async def reader(socket,counter):
    while True:
        # print('receiving...')
        name = await socket.recv()
        # print('received:', value)
        p = j.core.processmanager.startProcess(method=MyMethod,args={"hello":name.decode()},name=name.decode())
        counter+=1
        print(counter)

async def logger():
    counter=0
    while True:
        for key,p in j.core.processmanager.processes.items():
            p.sync()
            print(p.new_stdout)
        counter+=1
        await asyncio.sleep(1)
        print("logger:%s"%counter)


async def main(loop):
    await asyncio.wait([reader(socket,counter),logger()]),


socket = aionn.Socket(aionn.AF_SP, aionn.PULL)
socket.bind('tcp://*:5555')
loop = asyncio.get_event_loop()

loop.run_until_complete(main(loop))
