from datetime import datetime


def parse_date_from_filename(filename: str, /) -> datetime:
    date = f"{filename[2:4]}-{int(filename[4], base=16):02d}-{filename[5:7]}"
    hour = f"{filename[7:9]}:{filename[10:12]}:{filename[12:14]}"

    return datetime.strptime(f"{date}T{hour}", r"%y-%m-%dT%H:%M:%S")
