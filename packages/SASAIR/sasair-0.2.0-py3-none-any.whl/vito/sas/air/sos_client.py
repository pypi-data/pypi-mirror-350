
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Tuple, List, Set, Dict, Any

import requests
import urllib3
from cachetools import TTLCache, cached
from pydantic import BaseModel, Field

from vito.sas.air import logger
from vito.sas.air.api_client import RESTclient
from vito.sas.air.utils.date_utils import to_utc_iso, iso_utc_to_datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# docs: https://uk-air.defra.gov.uk/sos-ukair/static/doc/api-doc/

class Pollutant(BaseModel, frozen=True):
    name: str = Field(..., description="Unique name of the quantity")
    description: str = Field(..., description="Unique description of the quantity")

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.name} ({self.description})"


class Station(BaseModel, frozen=True):
    local_code: str
    description: str
    longitude: float
    latitude: float
    pollutants: List[Pollutant]  # List of pollutants

    def has_pollutant(self, pollutant_name: str) -> bool:
        """Check if this station measures the specified pollutant"""
        return any(p.name == pollutant_name for p in self.pollutants)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.local_code} - {self.description} (Lat: {self.latitude} - Lon: {self.longitude})"


class Observation(BaseModel, frozen=True):
    result_time: datetime  # This is the same as valid_time_end
    value: Optional[float]
    unit: Optional[str]
    meta_data: Optional[Dict[str, Any]] = Field(default=None)
    station_eoi_code: str
    pollutant_name: str

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{to_utc_iso(self.result_time)} {self.pollutant_name} at {self.station_eoi_code}: {self.value} {self.unit} )"


class PollutantEnum(str, Enum):
    """Enum for available pollutant types"""
    RELATIVE_HUMIDITY = "RH"
    CARBON_DIOXIDE = "CO2"
    WIND_SPEED_SCALAR = "WS"
    ELEMENTAL_GASEOUS_MERCURY = "HG0"
    PARTICULATE_MATTER_2_5 = "PM25"
    PARTICULATE_MATTER_1 = "PM1"
    BENZENE = "C6H6"
    NITROGEN_MONOXIDE = "NO"
    WIND_DIRECTION = "WD"
    TOLUENE = "C6H5CH3"
    BLACK_CARBON = "BC"
    ETHYLBENZENE = "C6H5C2H5"
    O_XYLENE = "O_C6H4_CH3_2"
    OZONE = "O3"
    PARTICULATE_MATTER_10 = "PM10"
    ATMOSPHERIC_PRESSURE = "AP"
    AMMONIA = "NH3"
    NITROGEN_DIOXIDE = "NO2"
    SULPHUR_DIOXIDE = "SO2"
    PARTICLE_NUMBER_100 = "PN100"
    MP_XYLENE = "MP_C6H4_CH3_2"
    TEMPERATURE = "T"
    CARBON_MONOXIDE = "CO"

    @classmethod
    def all(cls) -> List[str]:
        """Return all available pollutant types"""
        return [member.value for member in cls]


# Map pollutant names to SOS variable names (will be used as descriptions)
POLLUTANT_MAP: Dict[PollutantEnum, str] = {
    PollutantEnum.RELATIVE_HUMIDITY: "Relative Humidity",
    PollutantEnum.CARBON_DIOXIDE: "Carbon Dioxide",
    PollutantEnum.WIND_SPEED_SCALAR: "Wind Speed (scalar)",
    PollutantEnum.ELEMENTAL_GASEOUS_MERCURY: "Elemental gaseous mercury",
    PollutantEnum.PARTICULATE_MATTER_2_5: "Particulate Matter < 2.5 µm",
    PollutantEnum.PARTICULATE_MATTER_1: "Particulate Matter < 1 µm",
    PollutantEnum.BENZENE: "Benzene",
    PollutantEnum.NITROGEN_MONOXIDE: "Nitrogen monoxide",
    PollutantEnum.WIND_DIRECTION: "Wind Direction",
    PollutantEnum.TOLUENE: "Toluene",
    PollutantEnum.BLACK_CARBON: "Black Carbon",
    PollutantEnum.ETHYLBENZENE: "Ethylbenzene",
    PollutantEnum.O_XYLENE: "1,2-XYLENE O-XYLENE",
    PollutantEnum.OZONE: "Ozone",
    PollutantEnum.PARTICULATE_MATTER_10: "Particulate Matter < 10 µm",
    PollutantEnum.ATMOSPHERIC_PRESSURE: "Atmospheric  Pressure",
    PollutantEnum.AMMONIA: "Ammonia",
    PollutantEnum.NITROGEN_DIOXIDE: "Nitrogen dioxide",
    PollutantEnum.SULPHUR_DIOXIDE: "Sulphur dioxide",
    PollutantEnum.PARTICLE_NUMBER_100: "Number of particles < 100 nm",
    PollutantEnum.MP_XYLENE: "M+P-xylene",
    PollutantEnum.TEMPERATURE: "Temperature",
    PollutantEnum.CARBON_MONOXIDE: "Carbon Monoxide"
}

POLLUTANT_REVERSE_MAP = {description: pollutant for pollutant, description in POLLUTANT_MAP.items()}

# Cache settings
CACHE_TTL = 24 * 60 * 60  # 24 hours in seconds

_station_cache = TTLCache(maxsize=1, ttl=CACHE_TTL)
_pollutants_cache = TTLCache(maxsize=1, ttl=CACHE_TTL)


class SOSClient(RESTclient):
    """
    Client for the Sensor Observation Service (SOS) API

    This client provides access to air quality data from stations
    across Europe through the SOS API.
    """

    def __init__(self, base_url: Optional[str] = None, session: Optional[requests.Session] = None):
        """
        Initialize the SOS client.

        Args:
            base_url: The base URL of the SOS API. Defaults to "https://geo.irceline.be/sos/sos"
            session: The requests session to use. If None, a new session will be created.
        """
        super().__init__(base_url or "https://geo.irceline.be/sos/sos", session)
        logger.info(f"Initialized SOSClient with base URL: {self.base_url}")


    def get_observations(self, station_name: str, pollutant: str, start_time: datetime, end_time: datetime) -> List[Observation]:
        """
        Get observations for a specific station and pollutant within a time range.

        Args:
            station_name: The EOI code of the station
            pollutant: The name of the pollutant
            start_time: The start time of the observations
            end_time: The end time of the observations

        Returns:
            A list of observations

        Raises:
            ValueError: If the station or pollutant is not found
        """
        # Ensure times are in UTC
        time_zone = start_time.tzinfo
        if time_zone is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
            end_time = end_time.replace(tzinfo=timezone.utc)

        # Format to YYYY-MM-DDTHH:MM:SS.mmmZ
        start_time_iso = to_utc_iso(start_time)
        end_time_iso = to_utc_iso(end_time)

        logger.info(f"Getting observations for station {station_name}, pollutant {pollutant} "
                    f"from {start_time_iso} to {end_time_iso}")

        # Get stations and check if the requested station exists
        stations = self.get_stations_cached()
        if station_name not in stations:
            available_stations = ", ".join(stations.keys())
            error_msg = f"Station {station_name} not found. Available stations: {available_stations}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Get pollutants and check if the requested pollutant exists
        pollutants = self.get_pollutants_cached()
        if pollutant not in pollutants:
            available_pollutants = ", ".join(pollutants.keys())
            error_msg = f"Pollutant {pollutant} not found. Available pollutants: {available_pollutants}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        station: Station = stations[station_name]
        pollutant_obj: Pollutant = pollutants[pollutant]

        # Check if the station has the requested pollutant
        if not station.has_pollutant(pollutant):
            available_pollutants = ", ".join([p.name for p in station.pollutants])
            logger.warning(f"Station {station_name} does not measure pollutant {pollutant}. "
                           f"Available pollutants: {available_pollutants}")

        # Prepare request parameters
        params = self._base_params() | {
            "request": "GetObservation",
            "featureOfInterest": f"{station.local_code} - {station.description} - {pollutant_obj.description} - feature",
            "observedProperty": pollutant_obj.description,
            "temporalFilter": f"phenomenonTime,{start_time_iso}/{end_time_iso}"
        }

        # Execute request and parse response
        data = self._exec_get(self.base_url, params).json()
        observations = self._parse_observations(data, station_name, pollutant)

        logger.info(f"Retrieved {len(observations)} observations")
        return observations

    def _parse_observations(self, data: Dict[str, Any], station_eoi: str, pollutant_name: str) -> List[Observation]:
        """Parse observation data from API response"""
        observations: List[Observation] = []

        for observation in data.get('observations', []):
            identifier = observation.get('identifier', {})
            procedure = observation.get('procedure', "")
            offering = observation.get('offering', "")
            valid_time = observation.get('validTime', [])
            result = observation.get('result', {})

            unit: str = result.get('uom', "")
            value: Optional[float] = result.get('value', None)

            # Values <= -999 are considered missing
            if value is not None and value <= -999:
                value = None

            meta = {
                "identifier": identifier,
                "procedure": procedure,
                "offering": offering,
                "valid_time": valid_time
            }

            try:
                result_time_str = observation['resultTime']
                result_time =  iso_utc_to_datetime(result_time_str)
                observations.append(Observation(
                    result_time=result_time,
                    value=value,
                    unit=unit,
                    meta_data=meta,
                    station_eoi_code=station_eoi,
                    pollutant_name=pollutant_name
                ))
            except Exception as e:
                logger.error(f"Error parsing resultTime datetime ({result_time_str}): {e}. ")

        # Sort by valid_time_start
        observations.sort(key=lambda x: x.result_time)
        return observations

    def get_pollutants(self) -> Set[Pollutant]:
        """
        Get all available pollutants.

        Returns:
            A set of pollutants
        """
        logger.info("Getting all available pollutants")
        params = self._base_params() | {
            "request": "GetFeatureOfInterest"
        }
        data = self._exec_get(self.base_url, params).json()
        pollutants: Set[Pollutant] = set()

        for feature in data.get('featureOfInterest', []):
            _, _, pollutant = self._parse_identifier(feature.get('identifier', ""))
            if pollutant is not None:
                pollutants.add(pollutant)

        logger.info(f"Found {len(pollutants)} pollutants")
        return pollutants


    def get_stations(self) -> List[Station]:
        """
        Get all available stations.

        Returns:
            A list of stations
        """
        logger.info("Getting all available stations")
        params = self._base_params() | {
            "request": "GetFeatureOfInterest"
        }
        data = self._exec_get(self.base_url, params).json()
        stations: Dict[str, Station] = {}

        for feature in data.get('featureOfInterest', []):
            try:
                local_code, description, pollutant = self._parse_identifier(feature.get('identifier', ""))

                if pollutant is None:
                    continue

                # Parse station coordinates
                geometry = feature.get('geometry', {})
                if not geometry or 'coordinates' not in geometry:
                    logger.warning(f"No coordinates found for station {local_code}")
                    continue

                coordinates = geometry.get('coordinates', [0, 0])

                # Create new station or append pollutant to existing one
                if local_code not in stations:
                    stations[local_code] = Station(
                        local_code=local_code,
                        description=description,
                        longitude=coordinates[1],
                        latitude=coordinates[0],
                        pollutants=[pollutant]
                    )
                else:
                    # Check if pollutant already exists
                    existing_pollutants = [p.name for p in stations[local_code].pollutants]
                    if pollutant.name not in existing_pollutants:
                        stations[local_code].pollutants.append(pollutant)
            except Exception as e:
                logger.error(f"Error parsing station data: {e}")

        stations_list = list(stations.values())
        # Sort stations by eoi_code
        stations_list.sort(key=lambda x: x.local_code)

        logger.info(f"Found {len(stations_list)} stations")
        return stations_list

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get service capabilities.

        Returns:
            A dictionary with service capabilities
        """
        logger.info("Getting service capabilities")
        params = self._base_params() | {
            "request": "GetCapabilities"
        }
        return self._exec_get(self.base_url, params).json()

    @cached(_pollutants_cache)
    def get_pollutants_cached(self) -> Dict[str, Pollutant]:
        """
        Get all available pollutants (cached for 24 hours).

        Returns:
            A dictionary of pollutants indexed by name
        """
        set_pollutants = self.get_pollutants()
        pollutants = {pollutant.name: pollutant for pollutant in set_pollutants}
        return pollutants

    @cached(_station_cache)
    def get_stations_cached(self) -> Dict[str, Station]:
        """
        Get all available stations (cached for 24 hours).

        Returns:
            A dictionary of stations indexed by EOI code
        """
        list_stations = self.get_stations()
        stations = {station.local_code: station for station in list_stations}
        return stations

    def find_stations_with_pollutant(self, pollutant_name: str) -> List[Station]:
        """
        Find all stations that measure a specific pollutant.

        Args:
            pollutant_name: The name of the pollutant

        Returns:
            A list of stations that measure the pollutant
        """
        stations = self.get_stations_cached()
        return [station for station in stations.values() if station.has_pollutant(pollutant_name)]

    def _parse_identifier(self, identifier: str) -> Tuple[str, str, Optional[Pollutant]]:
        """Parse station and pollutant information from feature identifier"""
        if not identifier:
            return "", "", None

        try:
            parts = identifier.split(' - ')
            if len(parts) < 3:
                logger.warning(f"Invalid identifier format: {identifier}")
                return "", "", None

            eoi_code = parts[0].strip()
            poll_descr = parts[-2].strip()
            description = ' - '.join(parts[1:-2]).strip()

            pollutant = None
            if poll_descr not in POLLUTANT_REVERSE_MAP:
                logger.warning(f"Pollutant {poll_descr} not in supported list. "
                               f"Supported: {list(POLLUTANT_REVERSE_MAP.keys())}")
            else:
                poll = POLLUTANT_REVERSE_MAP[poll_descr]
                pollutant = Pollutant(name=str(poll.value), description=poll_descr)

            return eoi_code, description, pollutant
        except Exception as e:
            logger.error(f"Error parsing identifier '{identifier}': {e}")
            return "", "", None


    def _base_params(self) -> Dict[str, str]:
        """Get base parameters for API requests"""
        return {
            "service": "SOS",
            "version": "2.0.0",
        }

if __name__ == "__main__":
    """Example showing how to use the SOSClient"""
    from datetime import datetime, timedelta

    session = requests.Session()
    session.verify = False
    # Initialize client
    client = SOSClient(session=session)

    # Find all stations with NO2 measurements
    no2_stations = client.find_stations_with_pollutant(PollutantEnum.NITROGEN_DIOXIDE.value)
    print(f"Found {len(no2_stations)} stations measuring NO2")

    if no2_stations:
        # Get data for the first station
        station = no2_stations[0]
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=3)

        print(f"Getting NO2 data for station {station}")
        observations = client.get_observations(
            station.local_code,
            PollutantEnum.NITROGEN_DIOXIDE.value,
            start_time,
            end_time
        )

        print(f"Retrieved {len(observations)} observations")
        for obs in observations[:5]:  # Print first 5 observations
            print(obs)
