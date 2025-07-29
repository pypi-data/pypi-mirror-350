from __future__ import annotations

from dataclasses import dataclass

from remotivelabs.topology.control.request import ControlRequest, ControlRequestType


@dataclass
class PingRequest(ControlRequest):
    type: str = str(ControlRequestType.ping_v1)


@dataclass
class RebootRequest(ControlRequest):
    type: str = str(ControlRequestType.reboot_v1)
