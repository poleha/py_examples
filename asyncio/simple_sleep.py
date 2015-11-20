import asyncio
import time

@asyncio.coroutine
def sleepy():
    print("before sleep", time.time())
    yield from asyncio.sleep(5)
    print("after sleep", time.time())

asyncio.get_event_loop().run_until_complete(sleepy())