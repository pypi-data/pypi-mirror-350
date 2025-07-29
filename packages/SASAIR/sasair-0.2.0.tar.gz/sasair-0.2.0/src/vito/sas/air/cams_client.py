
import os
import shutil
import tempfile
import zipfile
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, date
from os import environ as envvars
from pathlib import Path
from typing import List, Optional, Dict, Union, Any

import cdsapi
import requests
from requests import Session
from requests.exceptions import RequestException

from vito.sas.air import logger
from vito.sas.air.utils.cams_utils import Pollutant, to_cams_variable

"""
CAMS Data Client

A Python client for downloading air quality forecast data from the Copernicus Atmosphere Monitoring Service (CAMS) using the CDS API.
"""


class BaseCAMSClient(ABC):
    """Abstract base class for CAMS clients with common functionality. """

    _date_format = '%Y-%m-%d'
    _cds_timeout = 600  # 10 minutes timeout

    def __init__(
            self,
            data_set: str,
            date_start: Optional[date] = None,
            forecast_days: int = 4,
            pollutant: Union[str, Pollutant] = Pollutant.NO2,
            verify_ssl: bool = True,
    ):
        """
        Initialize the base CAMS client

        Args:
            data_set (str): CAMS data set name
            date_start (date, optional): Start date for the forecast (defaults to today)
            forecast_days (int): Number of forecast days to fetch (1-4)
            pollutant (str or Pollutant): Pollutant to fetch data for
            verify_ssl (bool): Whether to verify SSL certificates

        Raises:
            ValueError: If invalid parameters are provided
        """
        # Validate pollutant
        if isinstance(pollutant, str):
            try:
                self.pollutant = Pollutant(pollutant.upper())
            except ValueError:
                valid_pollutants = ", ".join(Pollutant.all())
                raise ValueError(f"Invalid pollutant: {pollutant}. Choose from: {valid_pollutants}")
        else:
            self.pollutant = pollutant

        # Validate forecast days
        if forecast_days < 1 or forecast_days > 4:
            raise ValueError("forecast_days must be between 1 and 4")

        self.data_set = data_set
        self.date_start = date_start if date_start is not None else datetime.now().date()
        self.forecast_days = forecast_days
        self.verify_ssl = verify_ssl

    @abstractmethod
    def create_request_params(self) -> Dict[str, Any]:
        """
        Create request parameters for the CAMS API - must be implemented by subclasses

        Returns:
            Dict: Request parameters
        """
        pass

    @abstractmethod
    def get_file_name_base(self) -> str:
        """
        Generate a base file name for downloaded data - must be implemented by subclasses

        Returns:
            str: Base file name
        """
        pass

    @abstractmethod
    def download(
            self,
            destination_folder: Path,
            api_url: Optional[str] = None,
            api_key: Optional[str] = None,
            session: Optional[Session] = None,
            overwrite: bool = False,
            **kwargs
    ) -> Path:
        """
        Download CAMS forecast data - must be implemented by subclasses

        Args:
            destination_folder (Path): Folder to save the downloaded files
            api_url (str, optional): CAMS API URL
            api_key (str, optional): CAMS API key
            session (Session, optional): Requests session to use
            overwrite (bool): Whether to overwrite existing files

        Returns:
            Path: Path to the downloaded file
        """
        pass

    def _setup_cds_client(
            self,
            api_url: Optional[str] = None,
            api_key: Optional[str] = None,
            session: Optional[Session] = None
    ) -> cdsapi.Client:
        """
        Set up the CDS API client

        Args:
            api_url (str, optional): CAMS API URL
            api_key (str, optional): CAMS API key
            session (Session, optional): Requests session to use

        Returns:
            cdsapi.Client: Configured CDS client
        """
        # Create or use session
        if session is None:
            session = requests.Session()
            session.verify = self.verify_ssl

        # Create CDS client
        if api_key is None:
            logger.info("Using default CDS client configuration")

            # Check if environment variables are set for CDS API credentials
            if 'CDSAPI_URL' in os.environ and 'CDSAPI_KEY' in os.environ:
                logger.info("Using CDS API credentials from environment variables")
            else:
                logger.info("Using CDS API credentials from ~/.cdsapirc file")

            return cdsapi.Client(session=session, timeout=self._cds_timeout)
        else:
            logger.info(f"Using custom API URL: {api_url}")
            api_url = api_url or os.environ.get('CDSAPI_URL') or "https://ads.atmosphere.copernicus.eu/api"
            return cdsapi.Client(url=api_url, key=api_key, session=session, timeout=self._cds_timeout)



class CAMSMosClient(BaseCAMSClient):
    """
    CAMS Client for downloading 'cams-europe-air-quality-forecasts-optimised-at-observation-sites'
    from the Copernicus Atmosphere Monitoring Service (CAMS).

    This client supports downloading MOS-optimized forecast data for various pollutants.

    Example:

        >>>  from datetime import datetime
        >>>  from pathlib import Path
        >>>
        >>>  output_path = Path("./cams")
        >>>  today = datetime.now().date()
        >>>
        >>>  cams_client = CAMSMosClient(date_start=today, forecast_days=4)
        >>>  zip_file = cams_client.download(
        >>>     output_path,
        >>>     api_url="https://ads.atmosphere.copernicus.eu/api",
        >>>     api_key="your_api_key"
        >>>  )
        >>>  print(f"Downloaded data to {zip_file}")
    """

    def __init__(
            self,
            data_set: str = 'cams-europe-air-quality-forecasts-optimised-at-observation-sites',
            date_start: Optional[date | datetime] = None,
            include_station_metadata: bool = True,
            type: str = 'mos_optimised',
            country: str = 'belgium',
            forecast_days: int = 4,
            pollutant: Union[str, Pollutant] = Pollutant.NO2,
            verify_ssl: bool = True
    ):
        """
        Initialize a new CAMS MOS client

        Args:
            data_set (str): CAMS data set name
            date_start (date or datetime, optional): Start date for the forecast (defaults to today)
            include_station_metadata (bool): Whether to include station metadata
            type (str): Type of MOS optimization
            country (str): Country to get data for
            forecast_days (int): Number of forecast days to fetch (1-4)
            pollutant (str or Pollutant): Pollutant to fetch data for
            verify_ssl (bool): Whether to verify SSL certificates

        Raises:
            ValueError: If invalid parameters are provided
        """
        super().__init__(
            data_set=data_set,
            date_start=date_start,
            forecast_days=forecast_days,
            pollutant=pollutant,
            verify_ssl=verify_ssl,
        )

        self.include_station_metadata = include_station_metadata
        self.type = type
        self.country = country

    def create_request_params(self) -> Dict[str, Any]:
        """
        Create request parameters for the CAMS API

        Returns:
            Dict: Request parameters
        """
        year = self.date_start.year
        month = self.date_start.month
        day = self.date_start.day
        include_station_metadata_str = "yes" if self.include_station_metadata else "no"

        forecast_hours = self.forecast_days * 24
        leadtime_hour = [f"{x}-{x + 23}" for x in range(0, forecast_hours, 24)]
        cams_variable = to_cams_variable(self.pollutant)

        request_params = {
            'variable': [cams_variable],
            'country': [self.country],
            'type': [self.type],
            'leadtime_hour': leadtime_hour,
            'year': [str(year)],
            'month': [str(month).zfill(2)],
            'day': [str(day).zfill(2)],
            'include_station_metadata': include_station_metadata_str
        }
        return request_params

    def get_file_name_base(self) -> str:
        """
        Generate a base file name for downloaded data

        Returns:
            str: Base file name
        """
        date_start_str = self.date_start.strftime(self._date_format)
        date_end_str = (self.date_start + timedelta(days=self.forecast_days)).strftime(self._date_format)
        return f"cams_mos_{self.pollutant}_{date_start_str}_{date_end_str}"

    def download(
            self,
            destination_folder: Path | str,
            api_url: Optional[str] = None,
            api_key: Optional[str] = None,
            session: Optional[Session] = None,
            keep_zip: bool = False,
            overwrite: bool = False
    ) -> Path:
        """
        Download CAMS MOS forecast data

        Args:
            destination_folder (Path): Folder to save the downloaded files
            api_url (str, optional): CAMS API URL
            api_key (str, optional): CAMS API key
            session (Session, optional): Requests session to use
            keep_zip (bool): Whether to keep the downloaded zip file
            overwrite (bool): Whether to overwrite existing files

        Returns:
            Path: Path to the downloaded zip file

        Raises:
            FileExistsError: If the output file already exists and overwrite=False
            RequestException: If there's an issue with the download request
            Exception: For other errors during processing
        """
        # Create destination folder if it doesn't exist
        if not isinstance(destination_folder, Path):
            destination_folder = Path(str(destination_folder))
        destination_folder.mkdir(parents=True, exist_ok=True)

        # Get request parameters and generate filenames
        request_params = self.create_request_params()
        file_name = self.get_file_name_base()
        zip_file = destination_folder / f"{file_name}.zip"

        # Check if output file already exists
        if zip_file.exists() and not overwrite:
            logger.info(f"File {zip_file} already exists, skipping download")
            return zip_file

        try:
            # Create CDS client
            api_url = api_url or envvars.get('CAMS_CDS_API_URL')
            api_key = api_key or envvars.get('CAMS_CDS_API_KEY')
            cds_client = self._setup_cds_client(api_url, api_key, session)

            # Download data
            logger.info(f"Downloading CAMS MOS data for {self.pollutant} for {self.country}")
            cds_client.retrieve(self.data_set, request_params).download(zip_file)

            return zip_file

        except RequestException as e:
            logger.error(f"Request error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during CAMS download: {e}")
            if zip_file.exists():
                zip_file.unlink()
                logger.debug(f"Cleaned up zip file after error: {zip_file}")
            raise


class CAMSEuropeClient(BaseCAMSClient):
    """
    CAMS Client for downloading 'cams-europe-air-quality-forecasts' from the Copernicus Atmosphere
    Monitoring Service (CAMS).

    This client supports downloading forecast data for various pollutants and models.

    Example:

        >>>  from datetime import datetime
        >>>  from pathlib import Path
        >>>
        >>>  output_path = Path("./cams")
        >>>  today = datetime.now().date()
        >>>
        >>>  cams_client = CAMSEuropeClient(date_start=today, forecast_days=2)
        >>>  nc_file = cams_client.download(
        >>>     output_path,
        >>>     api_url="https://ads.atmosphere.copernicus.eu/api",
        >>>     api_key="your_api_key"
        >>>  )
        >>>  print(f"Downloaded data to {nc_file}")
    """

    # Default area for Belgium
    DEFAULT_AREA = [52, 2.5, 49, 6.5]

    def __init__(
            self,
            data_set: str = 'cams-europe-air-quality-forecasts',
            date_start: Optional[date] = None,
            cams_model_name: str = 'ensemble',
            forecast_days: int = 4,
            pollutant: Union[str, Pollutant] = Pollutant.NO2,
            area: Optional[List[float]] = None,
            verify_ssl: bool = True
    ):
        """
        Initialize a new CAMS Europe client

        Args:
            data_set (str): CAMS data set name
            date_start (date, optional): Start date for the forecast (defaults to today)
            cams_model_name (str): CAMS model name to use
            forecast_days (int): Number of forecast days to fetch (1-4)
            pollutant (str or Pollutant): Pollutant to fetch data for
            area (List[float], optional): Area coordinates [lat_max, lon_min, lat_min, lon_max],
                defaults to Belgium
            verify_ssl (bool): Whether to verify SSL certificates

        Raises:
            ValueError: If invalid parameters are provided
        """
        super().__init__(
            data_set=data_set,
            date_start=date_start,
            forecast_days=forecast_days,
            pollutant=pollutant,
            verify_ssl=verify_ssl,
        )

        # Validate model name
        europe_model_names = self.europe_model_names()
        if cams_model_name not in europe_model_names:
            raise ValueError(f"Invalid model name: {cams_model_name}. Choose from: {', '.join(europe_model_names)}")

        self.cams_model_name = cams_model_name
        self.area = area if area is not None else self.DEFAULT_AREA

    @classmethod
    def europe_model_names(cls) -> List[str]:
        """
        Returns a list of available CAMS model names

        Returns:
            List[str]: List of model names
        """
        return [
            "ensemble",
            "chimere",
            "dehm",
            "emep",
            "euradim",
            "gemaq",
            "lotos",
            "match",
            "minni",
            "mocage",
            "monarch",
            "silam"
        ]

    def create_request_params(self) -> Dict[str, Any]:
        """
        Create request parameters for the CAMS API

        Returns:
            Dict: Request parameters
        """
        formatted_date = self.date_start.strftime(self._date_format)
        date_str = f'{formatted_date}/{formatted_date}'
        forecast_hours = self.forecast_days * 24

        request_params = {
            'model': self.cams_model_name,
            'date': date_str,
            'format': 'netcdf_zip',
            'variable': to_cams_variable(self.pollutant),
            'level': '0',
            'type': 'forecast',
            'time': '00:00',
            'leadtime_hour': [str(x) for x in range(0, forecast_hours)],
            'area': self.area
        }
        return request_params

    def get_file_name_base(self) -> str:
        """
        Generate a base file name for downloaded data

        Returns:
            str: Base file name
        """
        date_start_str = self.date_start.strftime(self._date_format)
        date_end_str = (self.date_start + timedelta(days=self.forecast_days)).strftime(self._date_format)
        return f"cams_{self.cams_model_name}_{self.pollutant}_{date_start_str}_{date_end_str}"

    def download(
            self,
            destination_folder: Path,
            api_url: Optional[str] = None,
            api_key: Optional[str] = None,
            session: Optional[Session] = None,
            keep_zip: bool = False,
            overwrite: bool = False
    ) -> Path:
        """
        Download CAMS forecast data

        Args:
            destination_folder (Path): Folder to save the downloaded files
            api_url (str, optional): CAMS API URL
            api_key (str, optional): CAMS API key
            session (Session, optional): Requests session to use
            keep_zip (bool): Whether to keep the downloaded zip file
            overwrite (bool): Whether to overwrite existing files

        Returns:
            Path: Path to the downloaded NetCDF file

        Raises:
            FileExistsError: If the output file already exists and overwrite=False
            RequestException: If there's an issue with the download request
            Exception: For other errors during processing
        """
        # Create destination folder if it doesn't exist
        destination_folder.mkdir(parents=True, exist_ok=True)

        # Get request parameters and generate filenames
        request_params = self.create_request_params()
        file_name = self.get_file_name_base()
        zip_file = destination_folder / f"{file_name}.zip"
        netcdf_file = destination_folder / f"{file_name}.nc"

        # Check if output file already exists
        if netcdf_file.exists() and not overwrite:
            logger.info(f"File {netcdf_file} already exists, skipping download")
            return netcdf_file

        try:
            # Create CDS client
            api_url = api_url or envvars.get('CAMS_CDS_API_URL')
            api_key = api_key or envvars.get('CAMS_CDS_API_KEY')
            cds_client = self._setup_cds_client(api_url, api_key, session)

            # Download data
            logger.info(f"Downloading CAMS data for {self.pollutant} using {self.cams_model_name} model")
            cds_client.retrieve(self.data_set, request_params).download(zip_file)

            # Extract NetCDF file
            logger.info(f"Extracting NetCDF file from {zip_file}")
            netcdf_file = self._extract_netcdf_from_zip(zip_file, file_name)

            # Remove zip file if not keeping it
            if not keep_zip and zip_file.exists():
                zip_file.unlink()
                logger.debug(f"Removed zip file: {zip_file}")

            return netcdf_file

        except RequestException as e:
            logger.error(f"Request error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during CAMS download: {e}")
            if zip_file.exists():
                zip_file.unlink()
                logger.debug(f"Cleaned up zip file after error: {zip_file}")
            raise

    def _extract_netcdf_from_zip(self, zip_file: Path, file_name: str) -> Path:
        """
        Extract the NetCDF file from the zip file

        Args:
            zip_file (Path): Path to the zip file
            file_name (str): Base name for the output file

        Returns:
            Path: Path to the extracted NetCDF file

        Raises:
            FileNotFoundError: If zip file does not exist
            ValueError: If zip contains unexpected number of NetCDF files
        """
        if not zip_file.exists():
            raise FileNotFoundError(f"Zip file not found: {zip_file}")

        target_path = zip_file.parent / f"{file_name}.nc"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Extract all files to the temporary directory
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(tmp_path)

            # Find NetCDF files
            nc_files = list(tmp_path.glob("*.nc"))
            if not nc_files:
                raise ValueError(f"No NetCDF files found in {zip_file}")
            if len(nc_files) > 1:
                logger.warning(f"Multiple NetCDF files found in {zip_file}, using the first one")

            # Move the first NetCDF file to the target path
            shutil.move(str(nc_files[0]), target_path)
            logger.info(f"Extracted NetCDF file to {target_path}")

            return target_path
