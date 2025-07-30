from datetime import datetime, date
from typing import Union, Optional

from enemera.api.base import BaseCurveClient
from enemera.core.constants import BASE_URL
from enemera.core.response import APIResponse
from enemera.models.response_models import IPEXFlowResponse, IPEXFlowLimitResponse


class ItalyCommercialFlowsClient(BaseCurveClient):
    """Client for Italian commercial flows"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            market: str,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area_from: Optional[str] = None,
            area_to: Optional[str] = None
            ) -> APIResponse[IPEXFlowResponse]:
        """Get Italian commercial flows"""
        params = {
            'market': market,
            'date_from': date_from,
            'date_to': date_to,
            'area_from': area_from,
            'area_to': area_to
        }

        endpoint = '/italy/commercial_flows'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, IPEXFlowResponse)


class ItalyCommercialFlowLimitsClient(BaseCurveClient):
    """Client for Italian commercial flow limits"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            market: str,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area_from: Optional[str] = None,
            area_to: Optional[str] = None
            ) -> APIResponse[IPEXFlowLimitResponse]:
        """Get Italian commercial flow limits"""
        params = {
            'market': market,
            'date_from': date_from,
            'date_to': date_to,
            'area_from': area_from,
            'area_to': area_to
        }

        endpoint = '/italy/commercial_flow_limits'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, IPEXFlowLimitResponse)
