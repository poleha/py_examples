import asyncio

@asyncio.coroutine
def slow_operation(future):
    yield from asyncio.sleep(1)
    future.set_result('Future is done!')

loop = asyncio.get_event_loop()
future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))
loop.run_until_complete(future)
print(future.result())
loop.close()

#***************************

import asyncio



@asyncio.coroutine
def sleeper(sec):
    print('starting', sec)
    yield from asyncio.sleep(sec)
    print('finished', sec)
    return sec

@asyncio.coroutine
def test(sec):
    response = yield from sleeper(sec)
    print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([
                        test(5),
                        test(3),
                        test(4),
                        test(1),
                        test(2),

                                    ]))

"""
starting 3
starting 1
starting 5
starting 4
starting 2
finished 1
1
finished 2
2
finished 3
3
finished 4
4
finished 5
5
"""

#**********************************************]

import asyncio
import aiohttp

@asyncio.coroutine
def print_page(url):
    response = yield from aiohttp.request('GET', url)
    body = yield from response.read_and_close(decode=False)
    print(body)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([print_page('http://mail.ru'),
                                      print_page('http://ag.ru')]))

#*************************************]
import asyncio
import datetime

@asyncio.coroutine
def display_date(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        yield from asyncio.sleep(1)

loop = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
loop.run_until_complete(display_date(loop))
loop.close()

#******************************************
import asyncio

loop = asyncio.get_event_loop()

# an instance of EchoProtocol will be created for each client connection.
class EchoProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.transport.write(data)

    def connection_lost(self, exc):
        server.close()

# run the coroutine to establish the server connection, then keep running
# the event loop until the server is stopped.
server = loop.run_until_complete(loop.create_server(EchoProtocol, '127.0.0.1', 4444))
loop.run_until_complete(server.wait_closed())

"""
Simple echo server
This is a simple echo server, used for showing you how to start a server with a given protocol.
You can connect to it with telnet 127.0.0.1 4444. Everything you type into the telnet session will
 be sent back to you from the server.
"""



#**************************************************]
import asyncio
import time

@asyncio.coroutine
def sleepy():
    print("before sleep", time.time())
    yield from asyncio.sleep(5)
    print("after sleep", time.time())

asyncio.get_event_loop().run_until_complete(sleepy())


#************************************

import asyncio

@asyncio.coroutine
def my_coroutine(future, task_name, seconds_to_sleep=3):
    print('{0} sleeping for: {1} seconds'.format(task_name, seconds_to_sleep))
    yield from asyncio.sleep(seconds_to_sleep)
    future.set_result('{0} is finished'.format(task_name))


def got_result(future):
    print(future.result())

loop = asyncio.get_event_loop()
future1 = asyncio.Future()
future2 = asyncio.Future()

tasks = [
    my_coroutine(future1, 'task1', 3),
    my_coroutine(future2, 'task2', 1)]

future1.add_done_callback(got_result)
future2.add_done_callback(got_result)

loop.run_until_complete(asyncio.wait(tasks))
loop.close()

#*****************************

import asyncio

@asyncio.coroutine
def slow_operation(future):
    yield from asyncio.sleep(1)
    future.set_result('Future is done!')

def got_result(future):
    print(future.result())
    loop.stop()

loop = asyncio.get_event_loop()
future = asyncio.Future()
asyncio.async(slow_operation(future)) #makes Task from coroutine
future.add_done_callback(got_result)

try:
    loop.run_forever()
finally:
    loop.close()

#********************************

import asyncio

@asyncio.coroutine
def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print("Task %s: Compute factorial(%s)..." % (name, i))
        yield from asyncio.sleep(1)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))

loop = asyncio.get_event_loop()
tasks = [
    asyncio.async(factorial("A", 2)),
    asyncio.async(factorial("B", 3)),
    asyncio.async(factorial("C", 4))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

#********************************************

import asyncio

f1 = asyncio.Future()
f2 = asyncio.Future()


def check_result(future):
    res = future.result()
    if res == 2:
        loop.stop()


def print_result(future):
    res = future.result()
    print(res)


f1.add_done_callback(print_result)
f1.add_done_callback(check_result)

f2.add_done_callback(print_result)
f2.add_done_callback(check_result)


@asyncio.coroutine
def c(future, time):
    yield from asyncio.sleep(time)
    future.set_result(time)
    return


loop = asyncio.get_event_loop()

asyncio.async(c(f1, 2))
loop.create_task(c(f2, 1))

try:
    loop.run_forever()
except:
    loop.close()


#**********************************************