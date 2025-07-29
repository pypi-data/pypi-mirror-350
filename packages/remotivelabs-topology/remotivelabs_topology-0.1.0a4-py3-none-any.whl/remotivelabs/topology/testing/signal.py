from __future__ import annotations

from datetime import datetime

import remotivelabs.broker.sync as br


def get_values(signals: list[br.network_api_pb2.Signal]) -> list[float | int | bytes]:
    """
    Returns signal values
    """
    return list(map(_parse_value, signals))


def get_timestamp_as_datetime(signals: list[br.network_api_pb2.Signal]) -> list[datetime]:
    """
    Returns signal timestamps
    """
    return list(map(lambda s: datetime.fromtimestamp(s.timestamp / 1000000), signals))


def get_timestamp_micros(signals: list[br.network_api_pb2.Signal]) -> list[int]:
    """
    Returns signal timestamps, in microseconds
    """
    return list(map(lambda s: s.timestamp, signals))


def get_timestamp_ms(signals: list[br.network_api_pb2.Signal]) -> list[int]:
    """
    Returns signal timestamps, in milliseconds
    """
    return list(map(lambda s: int(s.timestamp / 1000), signals))


def get_timestamp_diffs(signals: list[br.network_api_pb2.Signal]) -> list[float]:
    """
    Returns diff between timestamps, in seconds
    """
    ts = get_timestamp_ms(signals)
    return [(ts[i] - ts[i - 1]) / 1000 for i in range(1, len(ts))]


def _parse_value(signal: br.network_api_pb2.Signal) -> float | int | bytes:
    v: float | int | bytes = getattr(signal, _parse_value_type(signal))
    return v


def _parse_value_type(signal: br.network_api_pb2.Signal) -> str:
    if signal.HasField("integer"):
        return "integer"
    if signal.HasField("double"):
        return "double"
    return "raw"
