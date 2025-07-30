"""
Main client interface for the Enemera API.

This module provides the primary client class (EnemeraClient) that serves as the
main entry point for interacting with the Enemera energy data API. It aggregates
all specialized clients for different data types and markets.
"""

from typing import Optional

import pandas as pd

from enemera.api import (
    ItalyPricesClient,
    ItalyXbidResultsClient,
    ItalyAncillaryServicesResultsClient,
    ItalyActDamDemandClient,
    ItalyFcsDamDemandClient,
    ItalyCommercialFlowsClient,
    ItalyCommercialFlowLimitsClient,

    ItalyGenerationClient,
    ItalyGenerationForecastClient,

    ItalyImbalanceDataClient, ItalyExchangeVolumesClient,
    ItalyLoadActualClient, ItalyLoadForecastClient,
    SpainPricesClient, SpainXbidResultsClient, ItalyImbalanceDataPT60MClient
)
from enemera.api.base import BaseCurveClient
from enemera.core.constants import BASE_URL
from enemera.core.response import APIResponse
from enemera.models.curves import Curve


class EnemeraClient(BaseCurveClient):
    """Main Enemera API client that aggregates all curve-specific clients.

    This is the primary entry point for interacting with the Enemera API.
    It provides access to all supported data curves through a unified interface,
    as well as convenience methods for retrieving data in different formats.

    Attributes:
        italy_prices: Client for Italian electricity prices
        italy_xbid_results: Client for Italian cross-border intraday results
        italy_exchange_volumes: Client for Italian energy exchange volumes
        italy_ancillary_services: Client for Italian ancillary services market
        italy_dam_demand_act: Client for Italian day-ahead market actual demand
        italy_dam_demand_fcs: Client for Italian day-ahead market forecasted demand
        italy_commercial_flows: Client for Italian commercial flows
        italy_commercial_flow_limits: Client for Italian commercial flow limits
        italy_load_actual: Client for Italian actual load data
        italy_load_forecast: Client for Italian load forecasts
        italy_generation: Client for Italian generation data
        italy_generation_forecast: Client for Italian generation forecasts
        italy_imbalance_data: Client for Italian imbalance data
        spain_prices: Client for Spanish electricity prices
        spain_xbid_results: Client for Spanish cross-border intraday results
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize a new EnemeraClient.

        Args:
            api_key: Optional API key for authentication. If not provided,
                the client will attempt to use the ENEMERA_API_KEY environment variable.
        """
        super().__init__(base_url=BASE_URL, api_key=api_key)

        # Initialize curve-specific clients
        self.italy_prices = ItalyPricesClient(api_key)
        self.italy_xbid_results = ItalyXbidResultsClient(api_key)
        self.italy_exchange_volumes = ItalyExchangeVolumesClient(api_key)
        self.italy_ancillary_services = ItalyAncillaryServicesResultsClient(
            api_key)
        self.italy_dam_demand_act = ItalyActDamDemandClient(api_key)
        self.italy_dam_demand_fcs = ItalyFcsDamDemandClient(api_key)

        self.italy_commercial_flows = ItalyCommercialFlowsClient(api_key)
        self.italy_commercial_flow_limits = ItalyCommercialFlowLimitsClient(
            api_key)

        self.italy_load_actual = ItalyLoadActualClient(api_key)
        self.italy_load_forecast = ItalyLoadForecastClient(api_key)

        self.italy_generation = ItalyGenerationClient(api_key)
        self.italy_generation_forecast = ItalyGenerationForecastClient(api_key)
        self.italy_imbalance_data = ItalyImbalanceDataClient(api_key)
        self.italy_imbalance_data_pt60m = ItalyImbalanceDataPT60MClient(api_key)

        self.spain_prices = SpainPricesClient(api_key)
        self.spain_xbid_results = SpainXbidResultsClient(api_key)

    def get(self, curve: Curve, **kwargs) -> APIResponse:
        """Get data for a specific curve.

        This is a generic method that uses the Curve enum to determine which
        specific client to use for retrieving data. It delegates the request to
        the appropriate specialized client based on the curve parameter.

        Args:
            curve: The data curve to retrieve
            **kwargs: Additional parameters to pass to the specialized client's get method
                (e.g., date_from, date_to, area, market, etc.)

        Returns:
            APIResponse: An enhanced list containing the API response data as model objects

        Raises:
            ValueError: If the specified curve is not supported

        Example:
            >>> client = EnemeraClient(api_key="your_api_key")
            >>> response = client.get(
            ...     Curve.ITALY_PRICES, 
            ...     market="MGP",
            ...     date_from="2023-01-01",
            ...     date_to="2023-01-31"
            ... )
        """
        curve_mapping = {
            Curve.ITALY_PRICES: self.italy_prices.get,
            Curve.ITALY_XBID_RESULTS: self.italy_xbid_results.get,
            Curve.ITALY_EXCHANGE_VOLUMES: self.italy_exchange_volumes.get,
            Curve.ITALY_ANCILLARY_SERVICES: self.italy_ancillary_services.get,
            Curve.ITALY_DAM_DEMAND_ACT: self.italy_dam_demand_act.get,
            Curve.ITALY_DAM_DEMAND_FCS: self.italy_dam_demand_fcs.get,

            Curve.ITALY_COMMERCIAL_FLOWS: self.italy_commercial_flows.get,
            Curve.ITALY_COMMERCIAL_FLOW_LIMITS: self.italy_commercial_flow_limits.get,

            Curve.ITALY_LOAD_ACTUAL: self.italy_load_actual.get,
            Curve.ITALY_LOAD_FORECAST: self.italy_load_forecast.get,

            Curve.ITALY_GENERATION: self.italy_generation.get,
            Curve.ITALY_GENERATION_FORECAST: self.italy_generation_forecast.get,

            Curve.ITALY_IMBALANCE_DATA: self.italy_imbalance_data.get,
            Curve.ITALY_IMBALANCE_DATA_PT60M: self.italy_imbalance_data_pt60m.get,

            Curve.SPAIN_PRICES: self.spain_prices.get,
            Curve.SPAIN_XBID_RESULTS: self.spain_xbid_results.get
        }

        if curve not in curve_mapping:
            raise ValueError(f"Unsupported curve: {curve}")

        return curve_mapping[curve](**kwargs)

    def get_pandas(self, curve: Curve, index_col: str = 'utc', naive_datetime: bool = False, **kwargs) -> pd.DataFrame:
        """
        Get data as pandas DataFrame

        Args:
            curve: The curve to query
            index_col: Column to use as DataFrame index (default: 'utc')
            naive_datetime: Whether to return naive datetime without timezone info
            **kwargs: Additional parameters to pass to the API

        Returns:
            pd.DataFrame: DataFrame containing the API response data
        """
        response = self.get(curve, **kwargs)
        return response.to_pandas(index_col=index_col, naive_datetime=naive_datetime)

    def get_pandas_cet(self, curve: Curve, naive_datetime: bool = False, **kwargs) -> pd.DataFrame:
        """
        Get data as pandas DataFrame with timestamps converted to CET timezone

        Args:
            curve: The curve to query
            naive_datetime: Whether to return naive datetime without timezone info
            **kwargs: Additional parameters to pass to the API

        Returns:
            pd.DataFrame: DataFrame containing the API response data with CET timezone
        """
        response = self.get(curve, **kwargs)
        return response.to_pandas_cet(naive_datetime=naive_datetime)
