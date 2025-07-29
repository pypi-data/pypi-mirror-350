from __future__ import annotations

from dataclasses import dataclass

from remotivelabs.topology.namespace import NamespaceName
from remotivelabs.topology.signal import SignalInfo, SignalName, SignalValue

__doc__ = "Structures and types to work with frames"

FrameName = str


@dataclass
class FrameInfo:
    """
    Metadata about a frame in a namespace.

    Attributes:
        name: Name of the frame.
        namespace: Namespace to which the frame belongs.
        signals: Dict of signal names and their corresponding SignalInfo.
        sender: List of entities that send this frame.
        receiver: List of entities that receive this frame.
        cycle_time_millis: Frame cycle time in milliseconds.
    """

    name: FrameName
    namespace: NamespaceName
    signals: dict[SignalName, SignalInfo]
    sender: list[str]
    receiver: list[str]
    cycle_time_millis: float

    def __str__(self) -> str:
        return f"{self.namespace}.{self.name}, signals={len(self.signals)}, cycle={self.cycle_time_millis}ms"


@dataclass(frozen=True)
class Frame:
    """
    A concrete instance of a frame carrying signal values.

    Attributes:
        name: Name of the frame.
        namespace: Namespace to which the frame belongs.
        timestamp: in micro seconds, set when first seen.
        signals: Dict with signal names with their current values.
        value: Raw or composite value associated with the frame (e.g., serialized representation).
    """

    timestamp: int
    name: FrameName
    namespace: NamespaceName
    signals: dict[str, SignalValue]
    value: SignalValue

    def __str__(self) -> str:
        return f"{self.namespace}.{self.name}: {self.value!r} @ {self.timestamp}µs, signals={list(self.signals.keys())}"


@dataclass(frozen=True)
class FrameSubscription:
    """
    Used to subscribe to a frame and optionally its signals.

    Attributes:
        name: Name of the frame to subscribe to.
        signals: List of signal names to subscribe to
                 - None: subscribe to all signals in the frame.
                 - []: subscribe to the frame without any signals.
    """

    name: str
    signals: list[SignalName] | None = None
