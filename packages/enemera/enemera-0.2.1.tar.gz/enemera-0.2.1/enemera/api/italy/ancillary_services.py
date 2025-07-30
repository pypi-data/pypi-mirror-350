from datetime import datetime, date
from typing import Union, Optional

from enemera.api.base import BaseCurveClient
from enemera.core.constants import BASE_URL
from enemera.core.response import APIResponse
from enemera.models.response_models import IPEXAncillaryServicesResponse


class ItalyAncillaryServicesResultsClient(BaseCurveClient):
    """Client for Italian electricity prices"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            market: str,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            market_segment: Optional[str] = None,
            area: Optional[str] = None) -> APIResponse[IPEXAncillaryServicesResponse]:
        """Get Italian XBID results"""

        params = {
            'market': market,
            'market_segment': market_segment,
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }
        endpoint = '/italy/ancillary_services'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, IPEXAncillaryServicesResponse)
