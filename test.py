# import aiohttp
# import asyncio

# async def get_info(URL, data):
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url=URL, json=data) as resp:
#             bebra = await resp.json()
#             return bebra
    
# async def start():
#     data = {
#         "tg_id" : 1893883161
#     }
#     a = await get_info("http://194.58.92.160:8000/api/get_agent_info/", data)
#     print(a)

# asyncio.run(start())
def zalupa():
    while 1:
        try:
            raise Exception(1)
        except Exception as e:
            print(e)
        finally:
            # continue
            print(3)

print(zalupa())