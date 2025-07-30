"""
Client for retrieving Italian electricity market prices.

This module provides a specialized client for accessing price data from
Italian electricity markets, including day-ahead and intraday markets.
"""

from datetime import datetime, date
from typing import Union, Optional

from enemera.api.base import BaseCurveClient
from enemera.core.constants import BASE_URL
from enemera.core.response import APIResponse
from enemera.models.response_models import PriceData


class ItalyPricesClient(BaseCurveClient):
    """Client for Italian electricity prices.

    This client provides access to price data from the Italian electricity markets,
    including day-ahead (MGP) and intraday markets (MI1-MI7).
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize a new ItalyPricesClient.

        Args:
            api_key: Optional API key for authentication
        """
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            market: str,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None) -> APIResponse[PriceData]:
        """Get Italian electricity prices.
        
        Retrieves price data from Italian electricity markets for a specified
        date range, market, and optionally filtered by bidding zone.
        
        Args:
            market: The market identifier (e.g., "MGP", "MI1", etc.)
                   Can be a string or Market enum value
            date_from: Start date for the data query (inclusive)
            date_to: End date for the data query (inclusive)
            area: Optional bidding zone filter (e.g., "NORD", "CSUD", etc.)
                 Can be a string or Area enum value
                 
        Returns:
            APIResponse[PriceData]: List-like object containing price data
            
        Example:
            >>> client = ItalyPricesClient(api_key="your_api_key")
            >>> prices = client.get(
            ...     market="MGP",
            ...     date_from="2023-01-01",
            ...     date_to="2023-01-31",
            ...     area="NORD"
            ... )
        """
        params = {
            'market': market,
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }
        endpoint = '/italy/prices'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, PriceData)
