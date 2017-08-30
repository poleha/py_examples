import asyncio
from aiohttp import ClientSession

async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()
            return response

loop = asyncio.get_event_loop()

tasks = [hello("http://httpbin.org/headers"), hello("http://httpbin.org/headers")]
tasks = [loop.create_task(task) for task in tasks]
wait = asyncio.wait(tasks)
loop.run_until_complete(wait)

for task in tasks:
    print(task.result().result())
