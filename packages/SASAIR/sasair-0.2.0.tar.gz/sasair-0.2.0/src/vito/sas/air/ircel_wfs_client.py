
from typing import Optional, Dict, List

import requests
from pydantic import BaseModel

from vito.sas.air import logger
from vito.sas.air.api_client import RESTclient


def get_string(dct: dict, key: str) -> str:
    """
    Get a string value from a dictionary, returning an empty string if the key is not found.
    """
    return str(dct.get(key, "")) or ""

# https://geo.irceline.be/realtime/ows?service=WFS&version=1.3.0&request=GetFeature&typeName=realtime:stations&outputFormat=json&srsName=EPSG:4326
#
# https://geo.irceline.be/realtime/ows?service=WFS&version=1.3.0&request=GetFeature&typeName=realtime:no2_hmean_station&outputFormat=json&srsName=EPSG:4326
#
# https://geo.irceline.be/realtime/ows?service=WFS&version=1.3.0&request=GetFeature&typeName=realtime:realtime:sos_station&outputFormat=json&srsName=EPSG:4326


class SosStation(BaseModel, frozen=True):
    sos_id: int
    local_code: str
    eoi_code: str
    zone_code: str
    area_type: str  # e.g. "urban", "rural"
    station_type: str # e.g. "background", "traffic" "industrial"
    description: str
    longitude: Optional[float]
    latitude: Optional[float]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.local_code} - {self.eoi_code} - {self.description} - {self.area_type} - {self.station_type} - {self.zone_code} (Lat: {self.latitude} - Lon: {self.longitude})"


class IrcelWfsClient(RESTclient):
    """
    Client for the IRCEL realtime WFS.
    """

    def __init__(self, base_url: Optional[str] = None, session: Optional[requests.Session] = None):
        super().__init__(base_url or "https://geo.irceline.be/realtime/ows", session)


    def _base_params(self) -> Dict[str, str]:
        """Get base parameters for API requests"""
        return {
            "service": "WFS",
            "version": "1.3.0",
            "outputFormat": "json"
        }

    def get_sos_stations(self) -> List[SosStation]:

        logger.info("Getting all available SOS stations")
        params = self._base_params() | {
            "request": "GetFeature",
            "typeName": "realtime:sos_station",
            "srsName": "EPSG:4326"
        }
        data = self._exec_get(self.base_url, params).json()
        features = data.get("features", [])
        return_list = []
        for feature in features:
            geometry = feature.get("geometry", {})
            station_coordinates = geometry.get("coordinates", [])
            if station_coordinates:
                lon = station_coordinates[0]
                lat = station_coordinates[1]
            else:
                lon , lat = None, None
            station_properties = feature.get("properties", {})

            sos_id: int = int(station_properties.get("station_id"))
            local_code: str = get_string(station_properties, "ab_local_code")
            eoi_code: str =  get_string(station_properties,"ab_eoi_code")
            zone_code: str =  get_string(station_properties,"ab_zone_code")
            name: str =  get_string(station_properties,"ab_name")
            description = name.replace(f"{local_code} -", '').strip()
            type_and_area = get_string(station_properties,"ab_area_type_of_station")
            if type_and_area:
                area_type, station_type = type_and_area.split(" - ")
            else:
                area_type = ''
                station_type = ''

            return_list.append(SosStation(
                sos_id=sos_id,
                local_code=local_code.upper(),
                eoi_code=eoi_code.upper(),
                zone_code=zone_code.upper(),
                area_type=area_type.upper(),
                station_type=station_type.upper(),
                description=description,
                longitude=lon,
                latitude=lat
            ))
        return return_list

# def get_capabilities(self) -> Dict[str, Any]: # https://geo.irceline.be/realtime/ows?service=WFS&version=1.3.0&request=GetCapabilities always returns XML
    #     """
    #     Get service capabilities.
    #
    #     Returns:
    #         A dictionary with service capabilities
    #     """
    #     logger.info("Getting service capabilities")
    #     params = self._base_params() | {
    #         "request": "GetCapabilities"
    #     }
    #     return self._exec_json_request(params)


if __name__ == "__main__":
    # Example usage
    session = requests.Session()
    session.verify = False
    wfs_client = IrcelWfsClient(session=session)
    stations = wfs_client.get_sos_stations()
    for station in stations:
        print(station)
