import asyncio

async def scheculed():
    await asyncio.sleep(1)
    print("World")

async def main():
    task = asyncio.create_task(scheculed())
    print("Hello")
    await asyncio.sleep(5)

asyncio.run(main())