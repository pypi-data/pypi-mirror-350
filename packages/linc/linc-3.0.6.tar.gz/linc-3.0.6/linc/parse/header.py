# type: ignore
from datetime import datetime

from ..models import Channel, DeviceId, Header, Laser
from ..utils import safe_get_list
from .constants import LICEL_DATE_FORMAT


def parse_header(header_list: list[bytes]) -> Header:
    l2 = header_list[1].split()
    l3 = header_list[2].split()
    l_channels = header_list[3:]

    lasers = parse_lasers(l3)
    channels = parse_channels(l_channels)

    return Header(
        filename=header_list[0],
        location=l2[0],
        start_date=datetime.strptime(
            f"{b' '.join(l2[1:3]).decode()}", LICEL_DATE_FORMAT
        ),
        stop_date=datetime.strptime(
            f"{b' '.join(l2[3:5]).decode()}", LICEL_DATE_FORMAT
        ),
        altitude=l2[5],
        longitude=l2[6],
        latitude=l2[7],
        zenith_angle=l2[8],
        azimuth_angle=safe_get_list(l2, 9, None),
        n_datasets=l3[4],
        lasers=lasers,
        channels=channels,
    )


def parse_lasers(lasers_line: list[bytes]) -> tuple[Laser]:
    if len(lasers_line) < 5:
        raise ValueError("Cannot parse lasers line from file")

    laser1 = Laser(shots=lasers_line[0], frecuency=lasers_line[1])
    laser2 = Laser(shots=lasers_line[2], frecuency=lasers_line[3])

    if len(lasers_line) == 5:
        return laser1, laser2

    laser3 = Laser(shots=lasers_line[5], frecuency=lasers_line[6])

    if len(lasers_line) == 7:
        return laser1, laser2, laser3
    elif len(lasers_line) == 9:
        laser4 = Laser(shots=lasers_line[7], frecuency=lasers_line[8])
        return laser1, laser2, laser3, laser4
    else:
        raise NotImplementedError("Unknown number of lasers tried to parse")


def parse_channels(channels_lines: list[bytes]) -> tuple[Channel]:
    channels: list[Channel] = []
    for line in channels_lines:
        pl = line.split()  # Properties list

        channel_physics = pl[7].split(b".")

        extension = channel_physics[-1].decode()
        #check extension to be a number:
        if not extension.isnumeric():
            polarization = extension
            wavelength = channel_physics[0].decode()            
        else:
            wavelength = pl[7].decode()
            polarization = 'o'
        channels.append(
            Channel(
                active=pl[0],
                type=pl[1],
                laser=pl[2],
                bins=pl[3],
                laser_polarization=pl[4].decode(),
                ptm_voltage=pl[5],
                binwidth=pl[6],
                wavelength=float(wavelength),
                polarization=polarization,
                adc_bits=pl[12],
                shots=pl[13],
                dc_dr=pl[14],
                device_id=parse_device_id(pl[15]),
            )
        )

    return tuple(channels)  # Tuple used to guarantee integrity


def parse_device_id(bytes_id: bytes) -> DeviceId:
    device_id = bytes_id.decode()
    sep_index = 3 if device_id.startswith("S2") else 2    
    return DeviceId(type=device_id[:sep_index], code=device_id[sep_index:])