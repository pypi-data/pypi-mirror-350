import asyncio

from remotivelabs.topology import (
    BehavioralModel,
    BrokerClient,
)


async def main():
    async with BrokerClient(url="http://127.0.0.1:50051") as broker_client:
        async with BehavioralModel(
            "BodyCanModule",
            broker_client=broker_client,
        ) as bm:
            await bm.run_forever()


if __name__ == "__main__":
    asyncio.run(main())
