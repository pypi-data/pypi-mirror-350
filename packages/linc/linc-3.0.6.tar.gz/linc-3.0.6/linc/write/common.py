from ..config import Config
from ..models import Channel, Header
from ..utils import device_id_to_str, safe_get_list, to_acquisition_type_string


def compare_joinable_dataset(header1: Header, header2: Header) -> None:
    assert header1.channels == header2.channels, (
        "While parsing a same dataset, channels most remain identical"
    )

    assert header1.location == header2.location, (
        "While parsing a same dataset, channels most remain identical"
    )


def get_merged_channel_config(channel: Channel, config: Config) -> Channel:
    channel_as_str = device_id_to_str(channel.device_id)
    channel_config = safe_get_list(
        list(filter(lambda c: c.link_to == channel_as_str, config.lidar.channels)),
        0,
        None,
    )

    if channel_config is None:
        return channel

    return Channel(**channel.model_copy(update=channel_config).model_dump_())  # type: ignore


def format_channel(channel: Channel, format: str) -> str:
    format = format.replace(r"%w", str(channel.wavelength))
    format = format.replace(r"%p", channel.polarization.value)
    format = format.replace(r"%a", to_acquisition_type_string(channel.device_id.type))
    format = format.replace(
        r"%i", f"{channel.device_id.type}{channel.device_id.number}"
    )

    return format
