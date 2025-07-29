from pathlib import Path


def read_file_header_dataset(file_path: Path | str) -> tuple[bytes, bytes]:
    _p = Path(file_path)

    with open(_p, "rb") as f:
        header, _, dataset = f.read().partition(b"\r\n\r\n")

    return header, dataset
