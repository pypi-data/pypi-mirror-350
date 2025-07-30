from datetime import datetime, date
from typing import Union, Optional

from enemera.api.base import BaseCurveClient
from enemera.core.constants import BASE_URL
from enemera.core.response import APIResponse
from enemera.models.response_models import ItalyImbalanceDataResponse


class ItalyImbalanceDataClient(BaseCurveClient):
    """Client for Italian imbalance data"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None) -> APIResponse[ItalyImbalanceDataResponse]:
        """Get Italian imbalance data"""
        params = {
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }
        endpoint = '/italy/imbalance/data'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, ItalyImbalanceDataResponse)


class ItalyImbalanceDataPT60MClient(BaseCurveClient):
    """Client for Italian imbalance data"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None) -> APIResponse[ItalyImbalanceDataResponse]:
        """Get Italian imbalance data"""
        params = {
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }
        endpoint = '/italy/imbalance/data_PT60M'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, ItalyImbalanceDataResponse)
