
# SASAIR (SAS Atmosphere Interface & Retrieval)

## Description

SASAIR is a Python package with Python client implementations for some common Air pollution and atmosphere related public API's.

Currently, it supports the following API's:
- SOS API (e.g.: https://geo.irceline.be/sos/)
- CAMS (Wrapper for the CDS API; https://ads.atmosphere.copernicus.eu/how-to-api)
- Realtime WFS (Partial implementation of the WFS API; https://geo.irceline.be/realtime/ows)

## Installation with pip

To install the package, you can use the following command:

```bash
pip install sasair 
```

## Building from Source

You need Conda to build the package from source. Follow these steps:

1. Clone the repository:

```bash
git clone https://git.vito.be/projects/MARVIN/repos/sasair
cd sasair
```
2. Create the Python environment:

```bash
conda env create --prefix ./.venv --file conda_env.yml
conda activate ./.venv
```
3. Install the package:

```bash
poetry install -E "full"
```

##  Modules Overview

### cams_client

Provides three primary client classes:
- **`CAMSMosClient`**: Downloads observation-site optimized forecasts (`mos_optimised`) for a given country and pollutant.
- **`CAMSEuropeClient`**: Downloads regional forecast data in NetCDF format for a specific CAMS model and pollutant.
- **`CAMSftpClient`**: Downloads CAMS data from the FTP server.

#### Common usage CAMSMosClient

```python
from datetime import datetime
from vito.sas.air.utils.cams_utils import Pollutant
from vito.sas.air.cams_client import CAMSMosClient

client = CAMSMosClient(date_start=datetime.now(), pollutant=Pollutant.NO2, country='belgium')
zip_file = client.download(destination_folder="./mos_data", api_key="your_api_key")
print(f"Downloaded MOS data to {zip_file}")
```

#### Common usage CAMSEuropeClient

```python
from datetime import datetime
from vito.sas.air.utils.cams_utils import Pollutant
from vito.sas.air.cams_client import CAMSEuropeClient

client = CAMSEuropeClient(date_start=datetime.now(), cams_model_name='ensemble', pollutant=Pollutant.NO2, area=None)  # Default area [52, 2.5, 49, 6.5] will be used.
nc_file = client.download(destination_folder="./cams_data", api_key="your_api_key")
print(f"Downloaded MOS data to {nc_file}")
```

**Notes:**
- Make sure you installed the cdsapi package: `pip install cdsapi` or pip install sasair[cds]`.
- You can enter the URL end API KEY in  the `~/.cdsapirc` file (as described in the [CDS API documentation](https://cds.climate.copernicus.eu/how-to-api)) to avoid passing them as parameters.

#### Common usage CAMSftpClient

```python
from vito.sas.air.cams_ftp_client import CAMSftpClient
from vito.sas.air.utils.cams_utils import Pollutant, crop_to_extent

client = CAMSftpClient(pollutant=Pollutant.PM25, ftp_host="aux.ecmwf.int", ftp_root="/DATA/CAMS_EUROPE_AIR_QUALITY")
nc_file = client.download(destination_folder="./cams_data", ftp_pw="**********")
print(f"Downloaded CAMS data to {nc_file}")
```

If you also want to crop the file to a specific extent, you can use the `crop_to_extent` function from the `cams_utils` module.
This function takes the input NetCDF file and crops it to the specified longitude and latitude bounds.

```python
from vito.sas.air.utils.cams_utils import crop_to_extent

cropped_file = nc_file.parent /  f"{nc_file.stem}_cropped.nc"
crop_to_extent(nc_file, cropped_file, lon_min=2.5, lon_max=6.5, lat_min=49, lat_max=52)

print(f"Cropped CAMS data: {cropped_file}")
```

**Notes:**
- Make sure you installed the xarray and netcdf4 packages: `pip install xarray netCDF4` or pip install sasair[xarray]`.
- You can set the FTP password as the 'CAMS_FTP_PW' environment variable to avoid passing them as parameters.  (Same for 'CAMS_FTP_USER', 'CAMS_FTP_HOST' and 'CAMS_FTP_ROOT_DIR' environment variables).


### ircel_wfs_client

Provides a `IrcelWfsClient` to retrieve station metadata from IRCEL’s realtime WFS endpoint.

Usage:
```python
from vito.sas.air.ircel_wfs_client import IrcelWfsClient

client = IrcelWfsClient()
stations = client.get_sos_stations()
for station in stations[:5]:
    print(station)
```

### sos_client

Provides a `SOSClient` to query air quality observations using the Sensor Observation Service.

Usage:
```python
from vito.sas.air.sos_client import SOSClient
from datetime import datetime, timedelta, timezone

client = SOSClient()
end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(days=3)

observations = client.get_observations(station_name="40DU07", pollutant="PM10", start_time=start_time, end_time=end_time)
for obs in observations:
    print(obs)
```

### api_client

Implements a generic `RESTclient` base class that wraps low-level GET/POST/PUT/DELETE methods with retry logic. It is extended by the IRCEL and SOS clients.

### date_utils

Utility functions for ISO 8601 datetime conversions:
- `to_utc_iso(datetime) -> str`: Convert datetime to UTC ISO string.
- `iso_utc_to_datetime(str) -> datetime`: Parse ISO string to UTC datetime.
- `is_valid_iso(str) -> bool`: Check if string is valid ISO format.


### Full API 

The full API documentation is available at [http://docs.marvin.vito.local/rma/sasair/](http://docs.marvin.vito.local/rma/sasair/).


## Contributing

If you want to contribute to spio, please follow the standard contributing guidelines and push your changes to a new branch in
https://git.vito.be/projects/MARVIN/repos/sasair


## CI/CD

The Jenkins pipeline is set up to automatically build and publish the Master branche to the PyPI server.

The Development and Master branches are automatically built and published to the Vito Artifactory (https://repo.vito.be/artifactory/api/pypi/marvin-projects-pypi-local).


## Contact

For questions or issues, please reach out to the project maintainers:

- **Roeland Maes**: [roeland.maes@vito.be](mailto:roeland.maes@vito.be)


## License

This project is licensed under the MIT License. See the `LICENSE.md` file for details.
