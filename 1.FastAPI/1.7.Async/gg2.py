import asyncio
async def fn():
	task=asyncio.create_task(fn2())
	print("one")
	#await asyncio.sleep(1)
	#await fn2()
	print('four')
	await asyncio.sleep(1)
	print('five')
	await asyncio.sleep(1)

async def fn2():
	#await asyncio.sleep(1)
	print("two")
	await asyncio.sleep(1)
	print("three")
	
asyncio.run(fn())
