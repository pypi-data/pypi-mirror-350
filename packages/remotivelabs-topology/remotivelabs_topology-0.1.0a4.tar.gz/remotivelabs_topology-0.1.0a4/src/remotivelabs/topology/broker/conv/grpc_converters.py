from __future__ import annotations

from typing import Union, cast

from remotivelabs.broker import common_pb2, network_api_pb2, restbus_api_pb2, system_api_pb2
from remotivelabs.topology import signal
from remotivelabs.topology.broker.restbus.signal_config import SignalConfig
from remotivelabs.topology.frame import Frame, FrameInfo
from remotivelabs.topology.namespace import NamespaceInfo, NamespaceName
from remotivelabs.topology.secoc import SecocCmac0, SecocFreshnessValue, SecocKey, SecocProperty, SecocTimeDiff
from remotivelabs.topology.signal import Signal, SignalInfo, SignalName, SignalValue, WriteSignal
from remotivelabs.topology.some_ip import RequestType, ReturnCode, SomeIPError, SomeIPEvent, SomeIPRequest, SomeIPResponse, _Meta


def value_to_network_value(v: SignalValue) -> network_api_pb2.Value:
    if signal.is_int(v):
        return network_api_pb2.Value(integer=v)
    if signal.is_float(v):
        return network_api_pb2.Value(double=v)
    if signal.is_binary(v):
        return network_api_pb2.Value(raw=v)
    return network_api_pb2.Value(strValue=v)


def tuple_to_signal_ids(items: list[tuple[NamespaceName, list[str]]]) -> network_api_pb2.SignalIds:
    return network_api_pb2.SignalIds(
        signalId=[
            common_pb2.SignalId(name=name, namespace=common_pb2.NameSpace(name=namespace)) for namespace, names in items for name in names
        ]
    )


# Namespace Conversions
def namespace_to_grpc(namespace: NamespaceName | NamespaceInfo) -> common_pb2.NameSpace:
    return common_pb2.NameSpace(name=namespace.name) if isinstance(namespace, NamespaceInfo) else common_pb2.NameSpace(name=namespace)


def namespace_to_grpc_namespaces(*namespace: NamespaceName) -> network_api_pb2.SignalIds:
    return common_pb2.Namespaces(items=[namespace_to_grpc(ns) for ns in namespace])


def signal_info_to_grpc(signal_info: SignalInfo) -> network_api_pb2.SignalIds:
    return common_pb2.SignalId(name=signal_info.name, namespace=common_pb2.NameSpace(name=signal_info.namespace))


def signal_infos_to_grpc(signal_infos: list[SignalInfo]) -> network_api_pb2.SignalIds:
    return network_api_pb2.SignalIds(signalId=[signal_info_to_grpc(signal_info) for signal_info in signal_infos])


def grpc_to_namespace_info(network_info: common_pb2.NetworkInfo) -> NamespaceInfo:
    return NamespaceInfo(name=network_info.namespace.name, type=network_info.type)


# Frame Conversions
def grpc_to_frame_info(frame_info: common_pb2.FrameInfo) -> FrameInfo:
    return FrameInfo(
        name=frame_info.signalInfo.id.name,
        namespace=frame_info.signalInfo.id.namespace.name,
        signals={signal.id.name: grpc_to_signal_info(signal) for signal in frame_info.childInfo},
        sender=frame_info.signalInfo.metaData.sender,
        receiver=frame_info.signalInfo.metaData.receiver,
        cycle_time_millis=frame_info.signalInfo.metaData.cycleTime,
    )


# Signal Conversions
def write_signal_to_grpc(namespace: NamespaceName, write_signal: WriteSignal) -> network_api_pb2.Signal:
    return network_api_pb2.Signal(
        id=common_pb2.SignalId(name=write_signal.name, namespace=common_pb2.NameSpace(name=namespace)),
        raw=write_signal.value if isinstance(write_signal.value, bytes) else None,
        integer=write_signal.value if isinstance(write_signal.value, int) else None,
        double=write_signal.value if isinstance(write_signal.value, float) else None,
        strValue=write_signal.value if isinstance(write_signal.value, str) else None,
    )


def signals_to_grpc(signals: list[Signal]) -> network_api_pb2.Signals:
    return network_api_pb2.Signals(
        signal=[
            network_api_pb2.Signal(
                id=common_pb2.SignalId(name=signal.name, namespace=common_pb2.NameSpace(name=signal.namespace)),
                raw=signal.value if isinstance(signal.value, bytes) else None,
                integer=signal.value if isinstance(signal.value, int) else None,
                double=signal.value if isinstance(signal.value, float) else None,
                strValue=signal.value if isinstance(signal.value, str) else None,
            )
            for signal in signals
        ]
    )


def grpc_to_signal(signal: network_api_pb2.Signal) -> Signal:
    value: int | float | bytes | str = signal.double
    if signal.raw != b"":
        value = signal.raw
    elif signal.HasField("integer"):
        value = signal.integer
    elif signal.HasField("strValue"):
        value = signal.strValue
    return Signal(
        name=signal.id.name,
        namespace=signal.id.namespace.name,
        value=value,
    )


def grpc_frame_to_signal_info(frame_info: common_pb2.FrameInfo) -> SignalInfo:
    return grpc_to_signal_info(frame_info.signalInfo)


def grpc_to_signal_info(signal_info: common_pb2.SignalInfo) -> SignalInfo:
    return SignalInfo(
        name=signal_info.id.name,
        namespace=signal_info.id.namespace.name,
        sender=signal_info.metaData.sender,
        receiver=signal_info.metaData.receiver,
        named_values=signal_info.metaData.namedValues,
        value_names={name: value for value, name in signal_info.metaData.namedValues.items()},
    )


# Property Conversions
def property_to_grpc(namespace: NamespaceName, prop: SecocProperty) -> system_api_pb2.PropertyValue:
    if isinstance(namespace, NamespaceInfo):
        namespace = namespace.name
    if isinstance(prop, SecocFreshnessValue):
        return system_api_pb2.PropertyValue(name="secoc_fv", scope=[namespace], raw=prop.fv)
    if isinstance(prop, SecocTimeDiff):
        return system_api_pb2.PropertyValue(name="secoc_timediff", scope=[namespace], double=prop.time_diff)
    if isinstance(prop, SecocKey):
        return system_api_pb2.PropertyValue(name="secoc_key", scope=[namespace, str(prop.key_id)], raw=prop.key)
    if isinstance(prop, SecocCmac0):
        return system_api_pb2.PropertyValue(name="secoc_cmac0", scope=[namespace], integer=1 if prop.enabled else 0)
    raise TypeError(f"Unsupported SecocProperty type: {type(prop).__name__}")


# Configuration Conversions
def write_signal_to_grpc_publisher_config(
    items: list[tuple[NamespaceName, list[WriteSignal]]], client_id: str
) -> network_api_pb2.PublisherConfig:
    signal_list = [write_signal_to_grpc(namespace, value) for namespace, values in items for value in values]
    return network_api_pb2.PublisherConfig(
        clientId=common_pb2.ClientId(id=client_id),
        signals=network_api_pb2.Signals(signal=signal_list),
    )


def signal_ids_to_grpc_subscriber_config(
    signals: list[tuple[NamespaceName, list[SignalName]]], client_id: str, on_change: bool, initial_empty: bool = False
) -> network_api_pb2.SubscriberConfig:
    return network_api_pb2.SubscriberConfig(
        clientId=common_pb2.ClientId(id=client_id), signals=tuple_to_signal_ids(signals), onChange=on_change, initialEmpty=initial_empty
    )


def signal_configs_to_grpc(items: list[tuple[NamespaceName, list[SignalConfig]]]) -> list[restbus_api_pb2.SignalSequence]:
    return [
        restbus_api_pb2.SignalSequence(
            id=common_pb2.SignalId(name=signal_config.name, namespace=namespace_to_grpc(namespace)),
            loop=[value_to_network_value(v) for v in signal_config.loop],
            initial=[value_to_network_value(v) for v in signal_config.initial],
        )
        for namespace, signal_configs in items
        for signal_config in signal_configs
    ]


def some_ip_request_to_signals(request: SomeIPRequest, client_id: int, session_id: int) -> list[WriteSignal]:
    """
    Convert a SomeIPRequest into a list of Signal objects.
    """
    base_name = f"{request.service_instance_name}.Request.{request.name}"
    signals: list[WriteSignal] = [
        WriteSignal(name=f"{base_name}.Meta.ClientID", value=client_id),
        WriteSignal(name=f"{base_name}.Meta.SessionID", value=session_id),
        WriteSignal(name=f"{base_name}.Meta.MessageType", value=request.message_type),
    ]

    if request.raw:
        signals.append(WriteSignal(name=base_name, value=request.raw))
    else:
        signals.extend([WriteSignal(name=f"{base_name}.{key}", value=value) for key, value in request.parameters.items()])

    return signals


def some_ip_response_to_signals(
    response: SomeIPResponse | SomeIPError,
    service_instance_name: str,
    method_name: str,
    meta: _Meta,
) -> list[WriteSignal]:
    """
    Convert a SomeIPResponse or SomeIPError into a list of Signal objects.
    """
    base_name = f"{service_instance_name}.Response.{method_name}"
    signals: list[WriteSignal] = [
        WriteSignal(name=f"{base_name}.Meta.ClientID", value=meta.client_id),
        WriteSignal(name=f"{base_name}.Meta.SessionID", value=meta.session_id),
    ]

    if isinstance(response, SomeIPResponse):
        signals.append(WriteSignal(name=f"{base_name}.Meta.ReturnCode", value=ReturnCode.E_OK))
        if response.raw:
            signals.append(WriteSignal(name=base_name, value=response.raw))
        else:
            signals.extend([WriteSignal(name=f"{base_name}.{key}", value=value) for key, value in response.parameters.items()])
    elif isinstance(response, SomeIPError):
        signals.append(WriteSignal(name=f"{base_name}.Meta.ReturnCode", value=response.return_code))

    return signals


def some_ip_event_to_signals(
    event: SomeIPEvent,
) -> list[WriteSignal]:
    signals: list[WriteSignal] = []
    base_name = f"{event.service_instance_name}.Event.{event.name}"

    if event.raw:
        signals.append(WriteSignal(name=base_name, value=event.raw))
    else:
        signals.extend([WriteSignal(name=f"{base_name}.{key}", value=value) for key, value in event.parameters.items()])

    return signals


def frame_to_some_ip_request(frame: Frame) -> tuple[SomeIPRequest, _Meta]:
    """
    Decode a frame to a SOME/IP request and metadata tuple
    """
    [service, name] = frame.name.split(".Request.", 2)
    signals = {param_name.replace(frame.name, "").strip("."): value for param_name, value in frame.signals.items()}

    # Make sure Meta signals are popped
    session_id = cast(int, signals.pop("Meta.SessionID"))
    client_id = cast(int, signals.pop("Meta.ClientID"))
    message_type = RequestType(cast(int, signals.pop("Meta.MessageType")))

    return (
        SomeIPRequest(
            name=name.strip("."), service_instance_name=service, parameters=signals, raw=cast(bytes, frame.value), message_type=message_type
        ),
        _Meta(session_id=session_id, client_id=client_id),
    )


def frame_to_some_ip_response(frame: Frame, signal_infos: dict[str, SignalInfo]) -> tuple[SomeIPResponse | SomeIPError, _Meta]:
    """
    Decode a grpc signals object into a response object.
    """
    signals = {param_name.replace(frame.name, "").strip("."): value for param_name, value in frame.signals.items()}

    # Extract Meta signals
    session_id = cast(int, signals.pop("Meta.SessionID"))
    client_id = cast(int, signals.pop("Meta.ClientID"))
    return_code = signals.pop("Meta.ReturnCode")

    rc = return_code
    if f"{frame.name}.Meta.ReturnCode" in signal_infos.keys():
        rc = signal_infos[f"{frame.name}.Meta.ReturnCode"].value_names.get(cast(str, return_code), return_code)

    if rc == ReturnCode.E_OK:
        return (
            SomeIPResponse(parameters=signals, raw=cast(bytes, frame.value)),
            _Meta(session_id=session_id, client_id=client_id),
        )

    return (
        SomeIPError(return_code=cast(Union[str, int], return_code)),
        _Meta(session_id=session_id, client_id=client_id),
    )


def frame_to_some_ip_event(frame: Frame) -> SomeIPEvent:
    """
    Decode a frame to a SOME/IP event
    """
    [service, name] = frame.name.split(".Event.", 2)
    signals = {param_name.replace(frame.name, "").strip("."): value for param_name, value in frame.signals.items()}

    return SomeIPEvent(
        raw=cast(bytes, frame.value),
        name=name.strip("."),
        service_instance_name=service,
        parameters=signals,
    )
