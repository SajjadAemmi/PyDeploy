import time
import asyncio
import random

count = 0

async def marriage(i):
    global count
    r = random.randint(0, 10)
    await asyncio.sleep(r)
    print(f"{i} married after {r} years")
    count += 1


async def main():
    for child in ["mamad", "gholi", "goli", "alex"]:
        asyncio.create_task(marriage(child))
    
    while count < 4:
        await asyncio.sleep(1)

if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"Executed in {elapsed:0.2f} seconds.")
