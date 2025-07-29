import asyncio

import patronus
from patronus.datasets import RemoteDatasetLoader

patronus.init()

DS_ID = "d-eo6a5zy3nwach69b"

async def main():
    remote_dataset = await RemoteDatasetLoader("simple-2").load()
    print(remote_dataset)

asyncio.run(main())

