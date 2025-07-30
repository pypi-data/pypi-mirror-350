from datetime import datetime, date
from typing import Union, Optional

from enemera.api.base import BaseCurveClient
from enemera.core.constants import BASE_URL
from enemera.core.response import APIResponse
from enemera.models.response_models import IPEXXbidRecapResponse


class ItalyXbidResultsClient(BaseCurveClient):
    """Client for Italian electricity prices"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None) -> APIResponse[IPEXXbidRecapResponse]:
        """Get Italian XBID results"""

        params = {
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }
        endpoint = '/italy/xbid/results'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, IPEXXbidRecapResponse)
