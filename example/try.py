import aiohttp
import asyncio
import async_timeout


async def get():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            # print(await resp.content.read(10))
            print(await resp.text())

loop = asyncio.get_event_loop()
loop.run_until_complete(get())
