from datetime import datetime, date
from typing import Union, Optional

from enemera.api.base import BaseCurveClient
from enemera.core.constants import BASE_URL
from enemera.core.response import APIResponse
from enemera.models.response_models import IpexQuantityResponse


class ItalyExchangeVolumesClient(BaseCurveClient):
    """Client for Italian exchange volumes"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            market: str,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None,
            purpose: Optional[str] = None) -> APIResponse[IpexQuantityResponse]:
        """Get Italian exchange volumes"""
        params = {
            'market': market,
            'date_from': date_from,
            'date_to': date_to,
            'area': area,
            'purpose': purpose
        }
        endpoint = '/italy/exchange_volumes'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, IpexQuantityResponse)
