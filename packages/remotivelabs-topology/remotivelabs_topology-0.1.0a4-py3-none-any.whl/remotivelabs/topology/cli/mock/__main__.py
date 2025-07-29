from __future__ import annotations

import argparse
import asyncio
import logging
import os
from argparse import ArgumentParser
from collections import defaultdict
from dataclasses import dataclass

from remotivelabs.topology.ecu_mock import ECUMock

_log = logging.getLogger(__name__)


def _parse_namespace_pair(pair: str) -> tuple[str, list[str]]:
    if "=" not in pair:
        raise argparse.ArgumentTypeError(f"Invalid format: '{pair}', expected NAMESPACE=ECU1,ECU2")
    namespace, ecu_str = pair.split("=", 1)
    if not namespace or not ecu_str:
        raise argparse.ArgumentTypeError(f"Empty namespace or ECU list in: '{pair}'")
    ecus = [e.strip() for e in ecu_str.split(",") if e.strip()]
    if not ecus:
        raise argparse.ArgumentTypeError(f"No valid ECUs in: '{pair}'")
    return namespace, ecus


@dataclass
class ECUMockArgs:
    """Command line argument parser.

    Attributes:
        namespaces: Dict where keys are ECU names and value is a list of namespaces.
        broker_url: URL of the broker.
        delay_multiplier: Multiply all delays with this value.
        log_level: Logging level.
    """

    namespaces: dict[str, list[str]]
    broker_url: str
    delay_multiplier: float
    log_level: int

    @staticmethod
    def parse() -> ECUMockArgs:
        parser = ArgumentParser(prog="ECUMock")
        parser.add_argument(
            "-n",
            "--namespaces",
            type=_parse_namespace_pair,
            action="append",
            required=True,
            metavar="NAMESPACE=ECU1,ECU2",
            help="Repeatable NAMESPACE=ECU1,ECU2 pairs (ECUs comma-separated)",
        )
        parser.add_argument(
            "-u",
            "--url",
            type=str,
            default=os.environ.get("REMOTIVE_BROKER_URL", "http://localhost:50051"),
            metavar="REMOTIVE_BROKER_URL",
        )
        parser.add_argument("-d", "--delay-multiplier", type=float, default=1.0)
        parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

        args = parser.parse_args()
        log_level = logging.DEBUG if args.verbose else logging.INFO

        ns_dict: dict[str, list[str]] = defaultdict(list)
        for namespace, ecus in args.namespaces:
            for ecu in ecus:
                ns_dict[ecu].append(namespace)
        return ECUMockArgs(namespaces=ns_dict, broker_url=args.url, delay_multiplier=args.delay_multiplier, log_level=log_level)


async def main(args: ECUMockArgs):
    _log.info(" > Starting ECUMock(s):\n%s", "\n".join(f"   {ecu}: {', '.join(ns)}" for ecu, ns in args.namespaces.items()))
    ecu = ECUMock(namespaces=args.namespaces, broker_url=args.broker_url, delay_multiplier=args.delay_multiplier)
    await ecu.run()


if __name__ == "__main__":
    ecu_args = ECUMockArgs.parse()
    logging.basicConfig(level=ecu_args.log_level, format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
    asyncio.run(main(ecu_args))
