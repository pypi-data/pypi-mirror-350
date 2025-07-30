from datetime import datetime, date
from typing import Union, Optional

from enemera.api.base import BaseCurveClient
from enemera.core.constants import BASE_URL
from enemera.core.response import APIResponse
from enemera.models.response_models import IPEXActualDemandResponse, IPEXEstimatedDemandResponse


class ItalyActDamDemandClient(BaseCurveClient):
    """Client for Italian DAM Demand Act or Fabbisogno"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None) -> APIResponse[IPEXActualDemandResponse]:
        """Get Italian Actual DAM Demand Act or Fabbisogno"""
        params = {
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }
        endpoint = '/italy/dam_demand/act'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, IPEXActualDemandResponse)


class ItalyFcsDamDemandClient(BaseCurveClient):
    """Client for Italian DAM Demand Fcs or Stima Fabbisogno"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None) -> APIResponse[IPEXEstimatedDemandResponse]:
        """Get Italian Actual DAM Demand FCS or Stima Fabbisogno"""
        params = {
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }
        endpoint = '/italy/dam_demand/fcs'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, IPEXEstimatedDemandResponse)
