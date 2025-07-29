import asyncio

from remotivelabs.topology import (
    BrokerClient,
    CanNamespace,
    RestbusConfig,
    filters,
)


async def main():
    async with (
        BrokerClient(url="http://127.0.0.1:50051") as broker_client,
        CanNamespace(
            "HazardLightControlUnit-DriverCan0",
            broker_client,
            restbus_configs=[RestbusConfig([filters.Sender(ecu_name="HazardLightControlUnit")])],
        ),
    ):
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
