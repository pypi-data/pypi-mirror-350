# Linc

<p align="center">
    <a href="https://pypi.org/project/linc" target="_blank">
        <img src="https://img.shields.io/pypi/v/linc?color=%2334D058&label=pypi%20package" alt="Package version">
    </a>
    <a href="https://pypi.org/project/linc" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/linc.svg?color=%2334D058" alt="Supported Python versions">
    </a>
</p>

---

Linc is a fast way to convert [Licel Raw Format](https://licel.com/raw_data_format.html) into netCDF4. Made for GFAT internal use but writer is highly customizable.

## Examples

### GFAT legacy writer

By default, the standard way to write a netCDF file is using the GFAT legacy writer. Assuming a directory with several measurement files, the conversion would be as follows.

```shell
measurements/
├─ RM2332919.194794
├─ RM2332919.184654
├─ RM2332919.204924
├─ RM2332919.215054
├─ ...
```

```python
from linc import write_nc_legacy
from linc.config import get_config

meas_path = Path("measurements")
meas_files = list(meas_path.glob("RM*"))

config = get_config("config.toml")

write_nc_legacy(
    meas_files,
    output_file,
    config=config,
)
```

### Using a custom writer
Linc have utilities to read and convert raw files data into Python objects. The simplest way to start is the `linc.reader.read_file`.

```python
from linc import write_nc_legacy
from linc.config import get_config

meas_path = Path("measurements")
meas_file = list(meas_path.glob("RM*"))[0] # A single file

config = get_config("config.toml")

current_file = read_file(meas_file, config=config)

# Header information
# Such as filename, location
# Laser list, Channel list, etc
print(current_file.header)


# Returns a Pandas dataframe which columns are the channels of the measurement
# and rows are bins.
print(current_file.dataset)
```

Then, you can create an iterative writer with nectCDF4 utitilities.

## Config file

Linc works with a configuration file that expects the following format:

```toml
# Lidar-specific parameters. Mandatory
[lidar]
bin_count = 16380
bin_width = 3.75
bins_per_microsecond = 40

# This are custom attributes that will be present in the final neCDF file. Not mandatory
[lidar.attrs]
location = "Granada"
system = "ALHAMBRA"
manufacturers = "Raymetrics"
overlap_is_corrected = "false"
BCK_MIN_ALT = 50000
BCK_MAX_ALT = 60000
```

Each channel has to be declared an linked to its device identificator this way:

```toml
[[lidar.channels]]
name = "signal_532xpa"
link_to = "BT0"

[[lidar.channels]]
name = "signal_532xpp"
link_to = "BC0"
```
