from datetime import date, datetime
from os import environ as envvars
from pathlib import Path
from typing import Optional, Tuple

from vito.sas.air import logger
from vito.sas.air.utils.cams_utils import Pollutant, to_cams_variable
from vito.sas.air.utils.digest import file_md5
from vito.sas.air.utils.remote_io import FtpIO

"""
Client for the CAMS Ftp server.
"""

# DEFAULT_AREA = [52, 2.5, 49, 6.5]


class CAMSftpClient():
    """
    Client for the CAMS Ftp server.

    Example usage:
        >>> from datetime import date
        >>> from pathlib import Path
        >>> from vito.sas.air.cams_ftp_client import CAMSftpClient
        >>>
        >>> cams_client = CAMSftpClient(date_start=datetime.now(), pollutant='NO2', ftp_host="aux.ecmwf.int", ftp_root="/DATA/CAMS_EUROPE_AIR_QUALITY")
        >>> local_file = cams_client.download(destination_folder=Path('/tmp'), overwrite=True)

    If you want to crop the downloaded file to a specific area, you can use the `crop_to_extent` function:
        >>> from vito.sas.air.utils.cams_utils import crop_to_extent
        >>> cropped_file = local_file.parent /  f"{local_file.stem}_cropped.nc"
        >>> crop_to_extent(local_file, cropped_file, lon_min=2.5, lon_max=6.5, lat_min=49, lat_max=52)
    """

    def __init__(
            self,
            cams_model_name: str = 'ensemble',
            date_start: Optional[date | datetime] = None,
            pollutant: str | Pollutant = Pollutant.NO2,
            # area: Optional[List[float]] = None,
            ftp_host: Optional[str] = None,
            ftp_user: Optional[str] = None,
            ftp_root: Optional[str] = None,

    ):
        """
        Args:
            cams_model_name: CAMS model name (default: 'ensemble')
            date_start: Start date for the forecast (default: today)
            pollutant: Pollutant to download (default: NO2)
            # area: Area to download (default: Leuven)
            ftp_host: FTP host (default: CAMS_FTP_HOST env var)
            ftp_user: FTP user (default: CAMS_FTP_USER env var)
            ftp_root: FTP root directory (default: CAMS_FTP_ROOT_DIR env var)
        """
        self.cams_model_name = cams_model_name
        self.date_start = date_start or datetime.now().date()
        self.pollutant = pollutant

        self.ftp_host = ftp_host or envvars.get("CAMS_FTP_HOST")
        self.ftp_user = ftp_user or envvars.get("CAMS_FTP_USER")
        self.ftp_root = Path(ftp_root or envvars.get("CAMS_FTP_ROOT_DIR"))

    def list_forecast_files(self, ftp_pw: Optional[str] = None):
        """
        List all forecast files for the given date and pollutant.
        Args:
            ftp_pw: FTP password (default: CAMS_FTP_PW env var)
        """
        remote_dir = self._remote_dir()
        with self._ftpio(ftp_pw=ftp_pw) as ftpio:
            return ftpio.list_files(remote_dir)

    def download(self,
                 destination_folder: Path | str,
                 overwrite: bool = False,
                 md5_check: bool = True,
                 ftp_pw: Optional[str] = None) -> Path:
        """
        Download the forecast file for the given date and pollutant.

        Args:
            destination_folder: Destination folder to download the file to
            overwrite: Overwrite the file if it already exists (default: False)
            md5_check: Check the md5 checksum of the downloaded file (default: True)
            ftp_pw: FTP password (default: CAMS_FTP_PW env var)

        Returns:
            Path: Path to the downloaded file
        """
        if not isinstance(destination_folder, Path):
            destination_folder = Path(str(destination_folder))
        destination_folder.mkdir(parents=True, exist_ok=True)
        remote_file = self._remote_file()
        local_file = destination_folder / remote_file.name

        if not overwrite and local_file.exists():
            logger.info(f"File {remote_file.name} already exists, skipping download")
        else:
            with self._ftpio(ftp_pw=ftp_pw) as ftpio:
                ftpio.download_file(remote_file, local_file.parent)
        # check the md5 checksum
        if md5_check:
            mds_ok, md5_local, md5_remote = self._md5_check(local_file, ftp_pw=ftp_pw)
            if not mds_ok:
                raise ValueError(
                    f"MD5 checksum failed for {local_file.name} md5_local: {md5_local} md5_remote: {md5_remote}")
        return local_file

    def _remote_dir(self) -> Path:
        date_str = self.date_start.strftime("%Y-%m-%d")
        cams_variable = to_cams_variable(self.pollutant)
        return self.ftp_root / 'forecast' / date_str / self.cams_model_name / cams_variable

    def _remote_file(self, file_type: str = 'nc', level: int = 0) -> Path:
        remote_dir = self._remote_dir()
        date_str = self.date_start.strftime("%Y-%m-%d")
        #eg: 'cams.eaq.forecast.ensemble.particulate_matter_2.5um.L0.2025-05-22.nc'
        file_name = f"cams.eaq.forecast.{self.cams_model_name}.{to_cams_variable(self.pollutant)}.L{level}.{date_str}.{file_type}"
        return remote_dir / file_name

    def _md5_check(self, local_file: Path, ftp_pw: Optional[str] = None) -> Tuple[bool, str, str]:
        md5_local = file_md5(local_file)

        date_str = self.date_start.strftime("%Y-%m-%d")
        md5_overview = self._remote_dir().parent / f"CAMS_{self.cams_model_name}_forecast_{date_str}.md5"

        with self._ftpio(ftp_pw=ftp_pw) as ftpio:
            ftpio.download_file(md5_overview, local_file.parent)
        md5_overview_local = local_file.parent / md5_overview.name

        # read the md5_overview_local line by line
        with open(md5_overview_local, 'r') as f:
            for line in f:
                line = line.strip()
                if line.endswith(local_file.name):
                    md5_remote = line.split(' ')[0].strip()
                    return md5_local == md5_remote, md5_local, md5_remote
        return False, md5_local, ''

    def _ftpio(self, ftp_pw: Optional[str] = None):
        pw = ftp_pw or envvars.get("CAMS_FTP_PW")
        return FtpIO(hostname=self.ftp_host)(pw=pw, user=self.ftp_user)


