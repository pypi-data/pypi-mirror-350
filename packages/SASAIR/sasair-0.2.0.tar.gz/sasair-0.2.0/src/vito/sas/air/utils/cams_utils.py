from enum import Enum
from pathlib import Path
from typing import List

from vito.sas.air import logger


class Pollutant(str, Enum):
    """Enum for pollutant types with string values"""
    NO2 = "NO2"
    PM10 = "PM10"
    PM25 = "PM25"
    O3 = "O3"

    @classmethod
    def all(cls) -> List[str]:
        """Return all available pollutant types"""
        return [member.value for member in cls]


# Map pollutant names to CAMS variable names
POLLUTANT_MAP = {
    Pollutant.NO2: "nitrogen_dioxide",
    Pollutant.PM10: "particulate_matter_10um",
    Pollutant.PM25: "particulate_matter_2.5um",
    Pollutant.O3: "ozone"
}


def to_cams_variable(pollutant: str) -> str:
    """
    Convert pollutant name to CAMS variable name

    Args:
        pollutant (str): Pollutant name (case-insensitive)

    Returns:
        str: CAMS variable name

    Raises:
        ValueError: If pollutant is not supported
    """
    try:
        # Handle case where pollutant is passed as Enum or string
        if isinstance(pollutant, Pollutant):
            return POLLUTANT_MAP[pollutant]
        return POLLUTANT_MAP[Pollutant(pollutant.upper())]
    except (KeyError, ValueError):
        valid_pollutants = ", ".join(Pollutant.all())
        raise ValueError(f"Unsupported pollutant: {pollutant}. Valid options are: {valid_pollutants}")



def crop_to_extent(cams_nc_file_in: Path, cams_nc_file_out: Path,
                   lon_min: float, lon_max: float, lat_min: float, lat_max: float):
    """
    Crop a CAMS netCDF file to a specified extent.
    Args:
        cams_nc_file_in (Path): Input netCDF file path
        cams_nc_file_out (Path): Output (cropped) netCDF file path (Overwrites if exists)
        lon_min (float): Minimum longitude
        lon_max (float): Maximum longitude
        lat_min (float): Minimum latitude
        lat_max (float): Maximum latitude

    Returns:
        None
    """
    import xarray as xr

    xr_ds = xr.load_dataset(str(cams_nc_file_in), engine='netcdf4')
    xr_ds = xr_ds.assign_coords({"longitude": (((xr_ds.longitude + 180) % 360) - 180)})

    # find the closest lat/lon values in the dataset
    min_lon = xr_ds.longitude.sel(longitude=lon_min, method='bfill').values
    max_lon = xr_ds.longitude.sel(longitude=lon_max, method='ffill').values

    min_lat = xr_ds.latitude.sel(latitude=lat_min, method='ffill').values
    max_lat = xr_ds.latitude.sel(latitude=lat_max, method='bfill').values

    cropped_dataset = xr_ds.sel(
        latitude=slice(max_lat, min_lat),
        longitude=slice(min_lon, max_lon)
    )

    # write the cropped dataset to a new nc file
    # output_file = cams_file.parent / f"{cams_file.stem}_cropped.nc"
    cams_nc_file_out.parent.mkdir(parents=True, exist_ok=True)
    if cams_nc_file_out.exists():
        logger.warning(f"File {cams_nc_file_out.name} already exists. Overwriting...")

    cropped_dataset.to_netcdf(str(cams_nc_file_out))