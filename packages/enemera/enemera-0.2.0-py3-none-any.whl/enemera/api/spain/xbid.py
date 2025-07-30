from datetime import datetime, date
from typing import Union, Optional

from enemera.api.base import BaseCurveClient
from enemera.core.constants import BASE_URL
from enemera.core.response import APIResponse
from enemera.models.response_models import SpainXbidResultsResponse


class SpainXbidResultsClient(BaseCurveClient):
    """Client for Spanish XBID results """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date]
            ) -> APIResponse[SpainXbidResultsResponse]:
        """Get Spanish XBID results"""

        params = {
            'date_from': date_from,
            'date_to': date_to,
        }
        endpoint = '/spain/xbid/results'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, SpainXbidResultsResponse)
