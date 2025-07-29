import time
from functools import wraps
from typing import Optional, Dict, Any

import requests

from vito.sas.air import logger


def retry_on_error(max_retries=3, delay=3):
    """Decorator for retrying functions on error"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Max retries reached for {func.__name__}: {e}")
                        raise
                    logger.warning(f"Request failed, retrying {func.__name__} in {delay} seconds. Error: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator


class RESTclient:
    """
    Base client for REST API's
    """

    def __init__(self, base_url: str, session: Optional[requests.Session] = None):
        self.base_url = base_url.rstrip('/')
        self.session = session if session is not None else requests.Session()

    def _base_params(self) -> Dict[str, str]:
        """Get base parameters for API requests"""
        return {}

    def _base_headers(self) -> Dict[str, str]:
        """Get base headers for API requests"""
        return {
            "Accept": "application/json"
        }

    def _build_url(self, *parts: str) -> str:
        return f"{self.base_url}/{'/'.join(part.strip('/') for part in parts)}"

    @retry_on_error()
    def _exec_get(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """Execute GET request and return the response"""
        get_headers = headers or self._base_headers()
        get_params = params or self._base_params()

        logger.debug(f"Making GET request to {url} with params: {params} session: {self.session}")
        return self.session.get(url, params=get_params, headers=get_headers, verify=self.session.verify, **kwargs)

    @retry_on_error()
    def _exec_post(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """Execute GET request and return the response"""
        get_headers = headers or self._base_headers()
        get_params = params or self._base_params()

        logger.debug(f"Making POST request to {url} with params: {params} session: {self.session}")
        return self.session.post(url, params=get_params, headers=get_headers, verify=self.session.verify, **kwargs)


    @retry_on_error()
    def _exec_put(self, url: str, params: Optional[Dict[str, Any]] = None,  headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """Execute GET request and return the response"""
        get_headers = headers or self._base_headers()
        get_params = params or self._base_params()

        logger.debug(f"Making PUT request to {url} with params: {params} session: {self.session}")
        return self.session.put(url, params=get_params, headers=get_headers, verify=self.session.verify, **kwargs)


    @retry_on_error()
    def _exec_delete(self, url: str, params: Optional[Dict[str, Any]] = None,  headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """Execute GET request and return the response"""
        get_headers = headers or self._base_headers()
        get_params = params or self._base_params()

        logger.debug(f"Making PUT request to {url} with params: {params} session: {self.session}")
        return self.session.delete(url, params=get_params, headers=get_headers, verify=self.session.verify, **kwargs)