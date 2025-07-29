from enum import Enum
from datetime import datetime

import pandas as pd
from pydantic import BaseModel, ConfigDict


class LaserPolarizationEnum(str, Enum):
    NONE = "0"
    VERTICAL = "1"
    HORIZONTAL = "2"
    RIGHT_CIRCULAR = "3"
    LEFT_CIRCULAR = "4"


class PolarizationEnum(str, Enum):
    NONE = "o"
    PARALLEL = "p"
    CROSSED = "s"
    RIGHT_CIRCULAR = "r"
    LEFT_CIRCULAR = "l"


class MeasurementTypeEnum(str, Enum):
    ANALOG = "BT"
    PHOTONCOUNTING = "BC"
    ANALOG_SQUARED = "S2A"
    PHOTONCOUNTING_SQUARED = "S2P"
    POWERMETER_PHOTODIODE = "PD"
    POWERMETER = "PM"


class FileTypeEnum(str, Enum):
    RAW_SIGNAL = "RS"
    DARK_CURRENT = "DC"
    TELECOVER = "TC"
    DESPOLARIZATION = "DP"


class Laser(BaseModel):
    shots: int
    frecuency: int


class DeviceId(BaseModel):
    code: str
    type: MeasurementTypeEnum


class Channel(BaseModel):
    active: bool
    laser: int
    bins: int
    laser_polarization: LaserPolarizationEnum = LaserPolarizationEnum.NONE
    ptm_voltage: int
    binwidth: float
    wavelength: int | float
    polarization: PolarizationEnum = PolarizationEnum.NONE
    adc_bits: int
    shots: int
    dc_dr: float  # Discriminator level () or data range
    device_id: DeviceId

    model_config = {
        "frozen": True,
    }


class Header(BaseModel):
    filename: str
    location: str
    start_date: datetime
    stop_date: datetime
    altitude: float
    longitude: float
    latitude: float
    zenith_angle: float
    azimuth_angle: float | None = None
    n_datasets: int
    lasers: list["Laser"]
    channels: list["Channel"]

    model_config = {"str_strip_whitespace": True, "frozen": True}

    # TODO: write custom validator for channels with associated lasers
    # @validator('channels')
    # def check_laser_on_channel(cls, v, _):
    #     return v


class DataFileU32(BaseModel):
    header: Header
    dataset: pd.DataFrame | pd.Series

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    # Validator not valid anymore since config files ...
    # @validator("dataset")
    # def dataset_length_must_match_header(cls, v, values):
    #     _header: Header = values["header"]

    #     # Header shape: (datasets x max bin of single profile)
    #     header_shape = (
    #         max(map(lambda x: x.bins, _header.channels)),
    #         _header.n_datasets,
    #     )
    #     if v.shape != header_shape:
    #         raise ValueError(
    #             f"Header shape: {header_shape} does not match with dataset shape {v.shape}"
    #         )

    #     return v


class DataFile(DataFileU32): ...
