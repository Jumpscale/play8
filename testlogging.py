import logging
import time
loggers=[]
for i in range(1000):
    logger=logging.getLogger(str(i))
    loggers.append(logger)
    logger.setLevel(logging.DEBUG)


class MyHandler(logging.Handler):
    def __init__(self):
        self.level=0
        logging.Handler.__init__(self)

    def emit(self,record):
        from IPython import embed
        print(9)
        embed()

handler=MyHandler()

# fh.setLevel(logging.DEBUG)

logger.addHandler(handler)


class Test():
    def een(self):
        print(1)
        logger.exception("test")

t=Test()
t.een()

time.sleep(100)
