from datetime import datetime, date
from typing import Optional, Union

from enemera.api.base import BaseCurveClient
from enemera.core.constants import BASE_URL
from enemera.core.response import APIResponse
from enemera.models.response_models import GenerationData


class ItalyGenerationClient(BaseCurveClient):
    """Client for Italian generation data"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            generation_type: str,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None) -> APIResponse[GenerationData]:
        """Get Italian generation data by source"""
        params = {
            'generation_type': generation_type,
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }
        endpoint = f'/italy/generation/actual'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, GenerationData)


class ItalyGenerationForecastClient(BaseCurveClient):
    """Client for Italian generation data"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            generation_type: str,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None) -> APIResponse[GenerationData]:
        """Get Italian generation forecast data by source"""
        params = {
            'generation_type': generation_type,
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }
        endpoint = f'/italy/generation/forecast'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, GenerationData)
