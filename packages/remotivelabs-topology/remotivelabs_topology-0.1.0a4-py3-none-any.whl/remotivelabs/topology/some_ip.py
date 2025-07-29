from __future__ import annotations

import enum
from dataclasses import dataclass, field

from remotivelabs.topology.signal import SignalValue

__doc__ = "Structures and types to work with SOME/IP"


class RequestType(enum.IntEnum):
    REQUEST = 0
    REQUEST_NO_RETURN = 1


class ReturnCode(enum.IntEnum):
    E_OK = 0
    E_NOT_OK = 1
    E_UNKNOWN_SERVICE = 2
    E_UNKNOWN_METHOD = 3
    E_NOT_READY = 4
    E_NOT_REACHABLE = 5
    E_TIMEOUT = 6
    E_WRONG_PROTOCOL_VERSION = 7
    E_WRONG_INTERFACE_VERSION = 8
    E_MALFORMED_MESSAGE = 9
    E_WRONG_MESSAGE_TYPE = 10


class ErrorReturnCode(enum.IntEnum):
    E_NOT_OK = 1
    E_UNKNOWN_SERVICE = 2
    E_UNKNOWN_METHOD = 3
    E_NOT_READY = 4
    E_NOT_REACHABLE = 5
    E_TIMEOUT = 6
    E_WRONG_PROTOCOL_VERSION = 7
    E_WRONG_INTERFACE_VERSION = 8
    E_MALFORMED_MESSAGE = 9
    E_WRONG_MESSAGE_TYPE = 10


ServiceName = str


@dataclass(frozen=True)
class SomeIPRequest:
    """
    Represents a SOME/IP request

    Attributes:
        name: The name of the request.
        service_instance_name: The name of the service associated with the request.
        raw: The raw data to be sent with the request. If non-empty, it takes priority over `parameters`.
        parameters:
            A dictionary of key-value pairs representing decoded request data.
            Note: `str` is only supported for named values (e.g., Enums).
    Note:
        When sending a request, if `raw` is non-empty, it overrides the contents of `parameters`.
    """

    name: str
    service_instance_name: ServiceName
    message_type: RequestType
    raw: bytes = b""
    parameters: dict[str, SignalValue] = field(default_factory=dict)


@dataclass(frozen=True)
class SomeIPRequestReturn(SomeIPRequest):
    message_type: RequestType = field(default=RequestType.REQUEST, init=False)


@dataclass(frozen=True)
class SomeIPRequestNoReturn(SomeIPRequest):
    message_type: RequestType = field(default=RequestType.REQUEST_NO_RETURN, init=False)


@dataclass
class SomeIPResponse:
    """
    Represents a SOME/IP response

    Attributes:
        raw: The raw data received in the response. If non-empty, it takes priority over `parameters`.
        parameters:
            A dictionary of key-value pairs representing decoded response data.
            Note: `str` is only supported for named values (e.g., Enums).

    Note:
        When processing a response, if `raw` is non-empty, it overrides the contents of `parameters`.
    """

    raw: bytes = b""
    parameters: dict[str, SignalValue] = field(default_factory=dict)


@dataclass
class SomeIPError:
    """
    Represents a SOME/IP error response

    Attributes:
        return_code: The return code of the response.
    """

    return_code: int | str


@dataclass
class SomeIPEvent:
    """
    Represents a SOME/IP event.

    Attributes:
        name: The name of the event.
        service_instance_name: The name of the service associated with the event.
        raw: Raw bytes of the event payload. If non-empty, it takes precedence over `parameters` when emitting an event.
        parameters:
            A dictionary of key-value pairs representing decoded event data.
            Note: `str` is only supported for named values (e.g., Enums).

    Note:
        When handling the event, if `raw` is non-empty, it overrides the contents of `parameters`.
    """

    name: str
    service_instance_name: ServiceName
    raw: bytes = b""
    parameters: dict[str, SignalValue] = field(default_factory=dict)


@dataclass(frozen=True)
class _Meta:
    session_id: int
    client_id: int
