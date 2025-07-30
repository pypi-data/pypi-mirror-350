"""
Enumeration of available data curves in the Enemera API.

This module defines the Curve enum which is used to identify which data series
to request from the API. Each enum value corresponds to a specific energy market dataset.
"""

from enum import Enum


class Curve(Enum):
    """Data curves available in the Enemera API.

    Each enum value represents a specific energy market dataset that can be
    retrieved from the API. These are used with the EnemeraClient.get() method
    to identify which data to request.
    """
    ITALY_PRICES = "italy_prices"  # Italian electricity market prices
    # Italian cross-border intraday results
    ITALY_XBID_RESULTS = "italy_xbid_results"
    # Italian energy exchange volumes
    ITALY_EXCHANGE_VOLUMES = "italy_exchange_volumes"
    # Italian ancillary services market results
    ITALY_ANCILLARY_SERVICES = "italy_ancillary_services"
    # Italian day-ahead market actual demand
    ITALY_DAM_DEMAND_ACT = "italy_dam_demand_act"
    # Italian day-ahead market forecasted demand
    ITALY_DAM_DEMAND_FCS = "italy_dam_demand_fcs"
    # Italian commercial flow limits
    ITALY_COMMERCIAL_FLOWS = "italy_commercial_flows"  # Italian commercial flows between zones
    ITALY_COMMERCIAL_FLOW_LIMITS = "italy_commercial_flow_limits"
    # Italian demand forecasts (Fabbisogno and Stime Fabbisogno)
    ITALY_DEMAND_FORECAST = "italy_demand_forecast"  # Italian demand forecasts
    ITALY_DEMAND_ACTUAL = "italy_demand_actual"  # Italian actual demand
    # Italian load data
    ITALY_LOAD_ACTUAL = "italy_load_actual"  # Italian actual load data
    ITALY_LOAD_FORECAST = "italy_load_forecast"  # Italian load forecasts
    # Italian generation forecasts
    ITALY_GENERATION = "italy_generation"  # Italian electricity generation data
    ITALY_GENERATION_FORECAST = "italy_generation_forecast"
    ITALY_IMBALANCE_DATA = "italy_imbalance_data"  # Italian imbalance data
    ITALY_IMBALANCE_DATA_PT60M = "italy_imbalance_data_pt60m"  # Italian imbalance data with 60-minute intervals (legacy data)
    ITALY_IMBALANCE_PRICES = "italy_imbalance_prices"  # Italian imbalance prices
    ITALY_IMBALANCE_VOLUMES = "italy_imbalance_volumes"  # Italian imbalance volumes
    # Spain Day-Ahead Market and Intraday Auction Market prices
    SPAIN_PRICES = "spain_prices"  # Spanish electricity market prices
    # Spanish cross-border intraday results
    SPAIN_XBID_RESULTS = "spain_xbid_results"
