# ncep-data-req

Download and preprocess NCEP GFS 0.25° atmospheric forecast data from NOAA using ASCII interface.

## Overview

This package provides utility functions to directly download and preprocess Global Forecast System (GFS) 0.25-degree resolution data from the NOAA NOMADS server. It supports extraction of pressure-level and surface-level variables for specific forecast hours, structured into usable `xarray.Dataset` objects.

## Features

- Access GFS 0.25° forecast data from NOAA
- Support for both pressure-level and surface variables
- Handles multiple or single forecast hours
- Outputs structured `xarray.Dataset` objects for easy analysis

## Installation

You can install the package from PyPI (after publishing):

```bash
pip install ncep_data_req

from ncep_data_req import get_data_preprocess, get_data_preprocess_s

# Example: Download temperature on pressure levels for 6 forecast hours
ds = get_data_preprocess(
    yy=2025, mm=5, dd=23, utc=0, ft=6, var='tmpprs', pvar='yes'
)

# Example: Download surface variable at one forecast hour
ds_surface = get_data_preprocess_s(
    yy=2025, mm=5, dd=23, utc=0, ft=3, var='tmp2m', pvar='no'
)


Parameters
yy, mm, dd: Year, month, day

utc: Initialization hour (0, 6, 12, or 18 UTC)

ft: Forecast hour (0 to 384 depending on GFS run)

var: GFS variable name (e.g., tmpprs, rhprs, ugrdprs, etc.)

pvar: 'yes' if pressure-level variable, 'no' for surface

Output
Returns an xarray.Dataset containing:

Dimensions: time/levels, lat, lon

Coordinates: pressure levels, lat/lon grid

Data variables: selected GFS variable 
check this link ( https://nomads.ncep.noaa.gov/dods/gfs_0p25_1hr/)


contact:subhrjitrath17@gmail.com

