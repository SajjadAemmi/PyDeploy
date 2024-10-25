import time
import random
import asyncio


async def get():
    print("Get file started...")
    r = random.randint(0, 10)
    await asyncio.sleep(r)
    print(f"Get file Ended in {r} seconds")


async def extract():
    print("Extract file started...")
    r = random.randint(0, 10)
    await asyncio.sleep(r)
    print(f"Extract file Ended in {r} seconds")


async def download():
    print("Download started...")
    await get()
    await extract()
    print("Download Ended")


async def printer():
    print("Printer started...")
    r = random.randint(0, 10)
    await asyncio.sleep(r)
    print(f"Printer Ended in {r} seconds")


async def ai_video():
    print("AI video started...")
    r = random.randint(0, 10)
    await asyncio.sleep(r)
    print(f"AI video Ended in {r} seconds")


async def ai_audio():
    print("AI audio started...")
    r = random.randint(0, 10)
    await asyncio.sleep(r)
    print(f"AI audio Ended in {r} seconds")


def ai_mix():
    print("AI mix started...")
    r = random.randint(0, 10)
    time.sleep(r)
    print(f"AI mix Ended in {r} seconds")


async def ai():
    print("AI started...")
    await asyncio.gather(
        ai_video(),
        ai_audio(),
    )
    ai_mix()
    print("AI Ended")


async def main():
    await asyncio.gather(
        download(),
        printer(),
        ai(),
    )
    print("Main Ended")


s = time.perf_counter()
asyncio.run(main())
elapsed = time.perf_counter() - s
print(f"Executed in {elapsed:0.2f} seconds.")
