from datetime import datetime, date
from typing import Optional, Union

from enemera.api.base import BaseCurveClient
from enemera.core.constants import BASE_URL
from enemera.core.response import APIResponse
from enemera.models.response_models import LoadData


class ItalyLoadActualClient(BaseCurveClient):
    """Client for Italian actual load"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None) -> APIResponse[LoadData]:
        """Get Italian actual load"""
        params = {
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }

        endpoint = '/italy/load/actual'

        response = self._make_request(endpoint, params)
        return self._parse_response(response, LoadData)


class ItalyLoadForecastClient(BaseCurveClient):
    """Client for Italian load forecasts"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None) -> APIResponse[LoadData]:
        """Get Italian load forecasts"""
        params = {
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }

        endpoint = '/italy/load/forecast'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, LoadData)
