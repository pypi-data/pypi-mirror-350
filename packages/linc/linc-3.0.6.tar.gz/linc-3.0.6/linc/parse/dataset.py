import numpy as np
import pandas as pd

from linc.utils import device_id_to_str

from ..models import Header


def parse_dataset(dataset: bytes, header: Header) -> pd.DataFrame:
    dt = np.dtype(np.uint32)
    dt = dt.newbyteorder("<")

    max_length = max(map(lambda x: x.bins, header.channels))
    _parsed = pd.DataFrame()

    for channel in header.channels:
        bytes_size = channel.bins * 4
        current_array = np.frombuffer(dataset, dtype=dt, count=channel.bins)
        # Use u
        _parsed[device_id_to_str(channel.device_id)] = np.pad(
            current_array, (0, max_length - current_array.shape[0]), "empty"
        )

        # parsed[idx, : current_array.shape[0]] = current_array

        *_, dataset = dataset[bytes_size:].partition(b"\r\n")
        # print("parsed: ")
        # print(parsed)
        # print(before, symbol)

    # WARNING: Do not erase the following line unless you know what you are doing
    _parsed = (
        _parsed / 1.0
    )  # Necesary to force all data to have float64 instead of uint32

    return _parsed
