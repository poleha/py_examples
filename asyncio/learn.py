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

import asyncio

@asyncio.coroutine
def sub_sleeper(sec):
    print('starting sub_sleeper', sec)
    return sec * 3

@asyncio.coroutine
def sleeper(sec):
    print('starting sleeper', sec)
    yield from asyncio.sleep(sec)
    res = yield from sub_sleeper(sec)
    print('finished sleeper', sec, res)
    return sec

@asyncio.coroutine
def test(sec):
    response = yield from sleeper(sec)
    print(response)
test6 = asyncio.async(test(6))


@asyncio.coroutine
def slow_operation(future):
    yield from asyncio.sleep(1)
    print('Finished slow_operation')
    future.set_result('Future is done!')

loop = asyncio.get_event_loop()
future = asyncio.Future()


loop = asyncio.get_event_loop()
asyncio.async(slow_operation(future))  #ensure_future in 3.5
loop.run_until_complete(asyncio.wait([
                        test(5),
                        test(3),
                        test(4),
                        test(1),
                        test(2),
                        test6,

                                    ]))
print(future.result())

"""
starting sleeper 6
starting sleeper 5
starting sleeper 3
starting sleeper 4
starting sleeper 1
starting sleeper 2
Finished slow_operation
starting sub_sleeper 1
finished sleeper 1 3
1
starting sub_sleeper 2
finished sleeper 2 6
2
starting sub_sleeper 3
finished sleeper 3 9
3
starting sub_sleeper 4
finished sleeper 4 12
4
starting sub_sleeper 5
finished sleeper 5 15
5
starting sub_sleeper 6
finished sleeper 6 18
6
Future is done!

"""
#****************************************************
import asyncio
import random


urls = ['http://mail.ru', 'http://ag.ru', 'http://lenta.ru']

@asyncio.coroutine
def get_url(url):
    wait_time = random.randint(1, 4)
    yield from asyncio.sleep(wait_time)
    print('Done: URL {} took {}s to get!'.format(url, wait_time))
    return url, wait_time


@asyncio.coroutine
def process_as_results_come_in():
    coroutines = [get_url(url) for url in urls]
    for coroutine in asyncio.as_completed(coroutines):
        """
        Another one is asyncio.as_completed, that takes a list of coroutines and returns an iterator that yields the
         coroutines in the order in which they are completed, so that when you iterate on it, you get each result as
         soon as it's available.
        """
        url, wait_time = yield from coroutine
        print('Coroutine for {} is done'.format(url))


@asyncio.coroutine
def process_once_everything_ready():
    coroutines = [get_url(url) for url in urls]
    results = yield from asyncio.gather(*coroutines)
    print(results)


def main():
    loop = asyncio.get_event_loop()
    print("First, process results as they come in:")
    loop.run_until_complete(process_as_results_come_in())
    print("\nNow, process results once they are all ready:")
    loop.run_until_complete(process_once_everything_ready())


if __name__ == '__main__':
    main()

#********************************** my
import asyncio

future1 = asyncio.Future()
future2 = asyncio.Future()

@asyncio.coroutine
def worker():
    future3 = loop.run_in_executor(None, non_coroutine_compute, 11000)
    asyncio.async(compute(future1, 10000)) #async, like new thread
    asyncio.async(compute(future2, 10))
    while True:
        res = yield from simple_compute(50) #like regular func call
        print(res)
        try:
            print(future1.result())
        except:
            pass
        try:
            print(future2.result())
        except:
            pass
        try:
            print(future3.result())
        except:
            pass
        yield from asyncio.sleep(3)

@asyncio.coroutine
def compute(future, val):
    max = 0
    for i in range(val):
        yield
        for j in range(val-1):
          #yield from asyncio.sleep(0.00001)
          if i - j > max:
              max = i - j
    future.set_result(max)

@asyncio.coroutine
def simple_compute(val):
    max = 0
    for i in range(val):
        yield
        for j in range(val-1):
          #yield from asyncio.sleep(0.00001)
          if i - j > max:
              max = i - j
    return max

def non_coroutine_compute(val):
    max = 0
    for i in range(val):
        for j in range(val-1):
          #yield from asyncio.sleep(0.00001)
          if i - j > max:
              max = i - j
    return max

loop = asyncio.get_event_loop()
#asyncio.async(compute(future1, 100))


asyncio.async(worker())

loop.run_forever()

loop.close()

#*************************************
import asyncio
from urllib.request import urlopen
import time
import selectors
import sys

start = time.time()
selector = selectors.DefaultSelector()
selector.register(sys.stdin, selectors.EVENT_READ)

results = []

@asyncio.coroutine
def line_reader(data):
    for line in data:
        print(line)
        yield from asyncio.sleep(10)

@asyncio.coroutine
def reader(url):
    try:
        data = urlopen(url)
        yield from line_reader(data)
    except ValueError:
        print('url not found: {}'.format(url))

@asyncio.coroutine
def counter(id):
    i = 0
    while True:
        i += 1
        print(id, i)
        yield from asyncio.sleep(1)



@asyncio.coroutine
def worker():
    while True:
        for key, mask in selector.select(0):
            line = key.fileobj.readline().strip()
            if line == 'exit':
                loop.close()
            asyncio.async(reader(line))
        yield

loop = asyncio.get_event_loop()
asyncio.async(counter('counter1'))
asyncio.async(counter('counter2'))
loop.run_until_complete(worker())