from typing import TypeVar, Iterator

from .models import DeviceId, MeasurementTypeEnum


U = TypeVar("U")
T = TypeVar("T", str, bytes)


def split_seq(seq: list[T], sep: T) -> Iterator[list[T]]:
    start = 0
    while start < len(seq):
        try:
            stop = start + seq[start:].index(sep)
            yield seq[start:stop]
            start = stop + 1
        except ValueError:
            yield seq[start:]
            break


def safe_get_list(list_input: list[U], idx: int, default: U | None) -> U | None:
    try:
        return list_input[idx]
    except IndexError:
        return default


def to_acquisition_type_string(type: MeasurementTypeEnum) -> str:
    match type:
        case MeasurementTypeEnum.ANALOG:
            return "a"
        case MeasurementTypeEnum.ANALOG_SQUARED:
            return "A"
        case MeasurementTypeEnum.PHOTONCOUNTING:
            return "p"
        case MeasurementTypeEnum.PHOTONCOUNTING_SQUARED:
            return "P"
        case _:
            raise ValueError("Input type not supported")


def device_id_to_str(device_id: DeviceId) -> str:
    return f"{device_id.type.value}{device_id.code}"


def str_to_device_id(device_id: str) -> DeviceId:
    sep_index = 3 if device_id.startswith("S2") else 2
    if len(device_id) < sep_index:
        raise ValueError(f"Invalid device id: {device_id}")
    return DeviceId(
        type=device_id[:sep_index],  # type: ignore
        code=device_id[sep_index:],  # type: ignore
    )
