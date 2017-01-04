import nnpy


# c=nnpy.Socket(nnpy.AF_SP,nnpy.REQ)
c=nnpy.Socket(nnpy.AF_SP,nnpy.PUSH)
# c=nnpy.Socket(nnpy.AF_SP,nnpy.REQREP)

# s2=nnpy.Socket(nnpy.AF_SP,nnpy.PAIR)
# c2=nnpy.Socket(nnpy.AF_SP,nnpy.PAIR)

c.connect('tcp://127.0.0.1:5555')

for i in range(10):
    c.send("proc%s"%i)
    # c.recv()
    # print(i)


# import asyncio
# import aionn
#
# socket = aionn.Socket(aionn.AF_SP, aionn.PUSH)
# socket.connect('tcp://127.0.0.1:5556')
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(socket.send('some data'))
