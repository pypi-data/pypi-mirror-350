# Zarr offline downloader

The idea is to have an option to download a zarr dataset for offline reuse or conversion to netcdf. The package is a command line tool and is not covering all kind of different zarr stores. It has been tested with Google Cloud Storage of ECMWF ERA5 reanalysis.

```sh
usage: zarr-downloader.py [-h] [--variable VARIABLE] [--offset OFFSET] [--verbose] 
                          [--to-netcdf] [--overwrite] url output

Download a zarr Array / Group from a URL

positional arguments:
  url                  URL to download from
  output               Output directory to save the zarr file

options:
  -h, --help           show this help message and exit
  --variable VARIABLE  Subset of variables to download. e.g. t2m,lon,lat,...
  --offset OFFSET      Offset for the chunk access pattern
  --verbose, -v        Verbose output
  --to-netcdf          Convert to netcdf
  --overwrite, -o      Overwrite existing files
```

## Examples

How to download a zarr dataset for offline reuse?

```sh
# Download ERA 5 surface 2m temperature from Google zarr store.
# There is an offset (chunks: 1000000.0)
# note t2m has two chunk dimensions: time,values
# this will download all chunks
zarr-downloader.py --offset 1000000,0 --variable t2m \
https://storage.googleapis.com/gcp-public-data-arco-era5/co/single-level-reanalysis.zarr-v2 \
/tmp/t2m
# this will download one chunk
zarr-downloader.py --offset 1000000,0 --size 1,1 --variable t2m \
https://storage.googleapis.com/gcp-public-data-arco-era5/co/single-level-reanalysis.zarr-v2 \
/tmp/t2m
# coordinates need to be downloaded completely
zarr-downloader.py --variable time,longitude,latitude \
https://storage.googleapis.com/gcp-public-data-arco-era5/co/single-level-reanalysis.zarr-v2 \
/tmp/t2m
```

after downloading one can open the full zarr dataset again, but access the downloaded parts:

```py
import zarr
import xarray as xr

ds = xr.open_zarr('/tmp/t2m')
ds
<xarray.Dataset>
Dimensions:              (time: 1323648, values: 542080)
Coordinates:
    depthBelowLandLayer  float64 ...
    entireAtmosphere     float64 ...
    latitude             (values) float64 ...
    longitude            (values) float64 ...
    number               int64 ...
    step                 timedelta64[ns] ...
    surface              float64 ...
  * time                 (time) datetime64[ns] 1900-01-01 ... 2050-12-31T23:0...
    valid_time           (time) datetime64[ns] ...
Dimensions without coordinates: values
Data variables: (12/38)
    cape                 (time, values) float32 ...
    d2m                  (time, values) float32 ...
    hcc                  (time, values) float32 ...
    istl1                (time, values) float32 ...
    istl2                (time, values) float32 ...
    istl3                (time, values) float32 ...
    ...                   ...
    tsn                  (time, values) float32 ...
    u10                  (time, values) float32 ...
    u100                 (time, values) float32 ...
    v10                  (time, values) float32 ...
    v100                 (time, values) float32 ...
    z                    (time, values) float32 ...
Attributes: (12/14)
    Conventions:               CF-1.7
    GRIB_centre:               ecmf
    GRIB_centreDescription:    European Centre for Medium-Range Weather Forec...
    GRIB_edition:              1
    GRIB_subCentre:            0
    history:                   2023-08-27T15:04 GRIB to CDM+CF via cfgrib-0.9...
    ...                        ...
    pangeo-forge:recipe_hash:  09c22f5fffc2fbe3742fbb38c8c2c761e1b41b50570f09...
    pangeo-forge:version:      0.9.5.dev2+gd43015b
    valid_time_start:          1940-01-01
    last_updated:              2025-05-12 03:32:06.266520+00:00
    valid_time_stop:           2025-02-28
    valid_time_stop_era5t:     2025-04-30

```

## Contribution

Follow the general rules of user contribution and politeness. Please open a ticket under [issues](https://gitlab.phaidra.org/imgw/zarr-downloader/-/issues).
