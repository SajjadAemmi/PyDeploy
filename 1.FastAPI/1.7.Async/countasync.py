import time
import asyncio
import random


async def marriage(i):
    r = random.randint(0, 10)
    await asyncio.sleep(r)
    print(f"{i} married after {r} years")


async def main():
    await asyncio.gather(marriage("mamad"), marriage("gholi"), marriage("goli"), marriage("alex"))


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"Executed in {elapsed:0.2f} seconds.")
