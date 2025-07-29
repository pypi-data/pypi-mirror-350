from pathlib import Path

import numpy as np
import pandas as pd

from .convertion import convert_to_physical_units
from .models import DataFileU32, DataFile
from .config import Config
from .parse.header import parse_header
from .parse.dataset import parse_dataset
from .parse.file import read_file_header_dataset


def read_file(file_path: str | Path, config: Config) -> DataFile:
    _p = Path(file_path)
    h, d = read_file_header_dataset(_p)
    header = parse_header(h.split(b"\r\n"))
    dataset = parse_dataset(d, header=header)

    file_u32 = DataFileU32(header=header, dataset=dataset)
    file = convert_to_physical_units(file_u32, config)

    if config is not None:
        new_dataset = replace_with_names(file.dataset, config)
        file = DataFile(header=header, dataset=new_dataset)

    return file


def replace_with_names(
    dataset: pd.DataFrame | pd.Series, config: Config
) -> pd.DataFrame | pd.Series:
    final_columns = list(map(lambda ch: ch.link_to, config.lidar.channels))
    # set_trace()

    if config.options.channel_not_present_all_ok:
        select_columns = list(filter(lambda ch: ch in dataset.columns, final_columns))
    else:
        select_columns = final_columns

    dataset = dataset[select_columns]

    for channel in config.lidar.channels:
        if channel.link_to in dataset.columns:
            if isinstance(dataset, pd.DataFrame):
                dataset = dataset.rename(columns={channel.link_to: channel.name})
            else:
                dataset = dataset.rename({channel.link_to: channel.name})
        else:
            if isinstance(dataset, pd.DataFrame):
                dataset.loc[:, channel.name] = np.nan
            else:
                dataset[:] = np.nan

    return dataset
