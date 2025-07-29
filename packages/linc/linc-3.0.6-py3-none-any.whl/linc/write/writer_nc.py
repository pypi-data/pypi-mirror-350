import time
import warnings
from importlib import metadata
from pathlib import Path
from typing import Any
from collections.abc import Iterable

import numpy as np
from rich.progress import Progress
from cftime import date2num

from ..models import DataFile
from ..reader import read_file
from ..config import Config
from ..config.models import LidarChannel
from ..parse.utils import parse_date_from_filename

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from netCDF4 import Dataset  # type: ignore


def write_nc_legacy(
    files: Iterable[Path | str],
    output_file: Path | str,
    config: Config,
) -> None:
    _f = sorted(list(files), key=lambda p: Path(p).name)

    nc = Dataset(output_file, "w")
    nc.history = "Created " + time.ctime(time.time())
    nc.generated_with = f"linc {metadata.version('linc')}"

    bin_width = config.lidar.bin_width
    bin_count = config.lidar.bin_count
    channel_array = np.array(filter_real_channels(config.lidar.channels))
    first_time = parse_date_from_filename(Path(_f[0]).name)

    _ = nc.createDimension("time", None)
    _ = nc.createDimension("range", config.lidar.bin_count)
    _ = nc.createDimension("channel", channel_array.shape[0])

    time_var = nc.createVariable("time", "i4", ("time",), compression="zlib")
    time_var.units = f"milliseconds since {first_time.isoformat().replace('T', ' ')}"
    time_var.calendar = "proleptic_gregorian"

    range_var = nc.createVariable("range", "f4", ("range",), compression="zlib")
    range_var[:] = np.arange(bin_width, bin_width * (bin_count + 1), bin_width)

    channel_var = nc.createVariable("channel", "S8", ("channel",))
    channel_var[:] = channel_array

    signal_vars = create_signal_variables(nc, config)  # Raw signal
    lidar_vars = create_lidar_vars(nc, config)
    # channels_vars = create_channels_vars(nc, config)

    progress = Progress()

    total_files = len(_f)
    total_digits = len(str(total_files))
    task1 = progress.add_task("[red]Processing...", total=len(_f))

    with progress:
        for idx_f, iter_file in enumerate(_f):
            current_file = read_file(iter_file, config=config)

            write_signal_vars(current_file, time_var, signal_vars, idx_f)
            write_lidar_vars(current_file, lidar_vars, idx_f)

            progress.update(
                task1,
                advance=1,
                description=f"[blue]Converting {idx_f + 1:0{total_digits}d}/{total_files} file",  # noqa: E501
            )
            # write_channels_vars(current_file, channel_array, channels_vars, idx_f)

    # progress.remove_task(task1)

    write_attrs(nc, config)

    nc.close()


def write_signal_vars(
    current_file: DataFile, time_var: Any, signal_vars: list[Any], index: int
) -> None:
    time_var[index] = date2num(
        current_file.header.start_date, units=time_var.units, calendar=time_var.calendar
    )
    for channel_str, channel_var in signal_vars:
        channel_var[index, :] = current_file.dataset[channel_str].values  # type: ignore


def write_attrs(nc: Any, config: Config) -> None:
    for k, v in config.lidar.attrs.items():
        set_or_create_attr(nc, attr_name=k, attr_value=v)


def create_signal_variables(nc: Any, config: Config) -> list[Any]:
    signal_vars: list[tuple[str, Any]] = []
    for channel in list(map(lambda x: x.name, config.lidar.channels)):
        channel_str = channel
        try:
            signal_var = nc.createVariable(
                f"{channel_str}",
                "f8",
                ("time", "range"),
                compression="zlib",
            )
        except Exception:
            raise ValueError(f"problem creating variable: {channel_str}")

        signal_vars.append((channel_str, signal_var))
    return signal_vars


def set_or_create_attr(var, attr_name, attr_value):
    if attr_name in var.ncattrs():
        var.setncattr(attr_name, attr_value)
        return
    try:
        var.UnusedNameAttribute = attr_value
        var.renameAttribute("UnusedNameAttribute", attr_name)
    except TypeError:
        raise TypeError(
            f"Type of attribute {attr_name} is {type(attr_value)} which cannot be written in netCDF"  # noqa: E501
        )
    return


def filter_real_channels(lidar_channels: list[LidarChannel]) -> list[str]:
    """This function retrieves the lidar channel regardless if stderr or signal.
    For example, if there are two LidarChannel signal_532xpa and stderr_532xpa, it only returns 532xpa to channels list

    Args:
        lidar_channels (list[LidarChannel]): list of config sourced channels

    Returns:
        list[str]: strings with the convention wavelenght|telescope|polarization|aq_type. Ej: 532xpa
    """  # noqa: E501
    channels: set[str] = set({})

    for lidar_channel in lidar_channels:
        channels |= {lidar_channel.name.split("_")[1]}

    return list(channels)


def create_lidar_vars(nc, config: Config) -> list[tuple[str, Any]]:
    lidar_vars: list[tuple[str, Any]] = []
    for opt_var in config.options.time_lidar_variables:
        lidar_var = nc.createVariable(
            opt_var.name,
            opt_var.type,
            ("time",),
            compression="zlib",
        )
        lidar_vars.append((opt_var.name, lidar_var))
    return lidar_vars


# def create_channels_vars(nc: Any, config: Config) -> list[tuple[str, Any]]:
#     channels_vars: list[tuple[str, Any]] = []
#     for opt_var in config.options.time_channel_variables:
#         channels_var = nc.createVariable(
#             opt_var.name,
#             opt_var.type,
#             ("time", "channel"),
#             compression="zlib",
#         )
#         channels_vars.append((opt_var.name, channels_var))
#     return channels_vars


def write_lidar_vars(
    current_file: DataFile, lidar_vars: list[tuple[str, Any]], index: int
) -> None:
    for lidar_var in lidar_vars:
        value = getattr(current_file.header, lidar_var[0])
        lidar_var[1][index] = value
