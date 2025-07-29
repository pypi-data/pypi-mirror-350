from typing import Any

from pydantic import BaseModel, Field


DEFAULT_ATTRS: dict[str, Any] = {"generated_by": "linc-python"}


class OptionalVariable(BaseModel):
    name: str
    type: str


class Options(BaseModel):
    channel_not_present_all_ok: bool = False
    time_lidar_variables: list[OptionalVariable] = []
    time_channel_variables: list[OptionalVariable] = []


class LidarChannel(BaseModel):
    name: str
    link_to: str  # The device ID


class LidarConfig(BaseModel):
    bin_width: float
    bin_count: int
    bins_per_microsecond: float = 20
    attrs: dict[str, Any] = DEFAULT_ATTRS
    channels: list[LidarChannel] = Field(default_factory=list)


class Config(BaseModel):
    lidar: LidarConfig = Field()
    options: Options = Field()


"""
DEFAULT_CONFIG: Config = {
    "lidar": {
        "attrs": {"converter": "linc"},
        "channels": [
            # {"wavelength": 532, "link_to": "BT0"},
            # {"wavelength": 532, "link_to": "S2A0"},
            # {"wavelength": 532, "link_to": "BT1"},
            # {"wavelength": 532, "link_to": "S2A1"},
        ],
    },
    "config": {
        "include_undefined_channels": True,
        "default_channel_name_format": r"%wx%p%a",
    },
}
"""
