"""
Response models for the Enemera API.

This module defines the data models for the various response types returned by the API.
Each model is a Pydantic model that validates and structures the raw JSON data.
The models are organized in a hierarchy, with BaseTimeSeriesResponse as the root.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Base models
class BaseTimeSeriesResponse(BaseModel):
    """Base model for all time series responses.

    All response models inherit from this base class, which provides
    the common UTC timestamp field present in all API responses.

    Attributes:
        utc: The UTC timestamp for the data point
    """
    utc: datetime = Field(..., description="UTC timestamp")


class BaseTimeSeriesWithResolutionResponse(BaseModel):
    """Base model for all time series responses.

    All response models inherit from this base class, which provides
    the common UTC timestamp field present in all API responses.

    Attributes:
        utc: The UTC timestamp for the data point
    """
    utc: datetime = Field(..., description="UTC timestamp")
    # time_resolution: str = Field(..., description="Time resolution (PT60M, PT15M)")
    time_resolution: Optional[str] = Field(None, description="Time resolution (PT60M, PT15M)")


class PriceData(BaseTimeSeriesWithResolutionResponse):
    """Model for electricity price data.

    This model represents price data from electricity markets,
    including day-ahead and intraday markets.

    Attributes:
        market: The market identifier (e.g., MGP, MI1)
        zone: The bidding zone identifier (e.g., NORD, CSUD)
        price: The electricity price in EUR/MWh
    """
    market: str = Field(..., description="Market identifier")
    zone: str = Field(..., description="Zone identifier")
    price: float = Field(..., description="Price in EUR/MWh")


class IPEXXbidRecapResponse(BaseTimeSeriesWithResolutionResponse):
    """Model for Italian Power Exchange (IPEX) cross-border intraday market (XBID) recap data.

    This model represents summary statistics for the continuous intraday market,
    including price ranges and volumes.

    Attributes:
        zone: The bidding zone identifier (e.g., NORD, CSUD)
        time_resolution: The time resolution of the data (e.g., PT60M, PT15M)
        first_price: The first observed price in EUR/MWh
        last_price: The last observed price in EUR/MWh
        min_price: The minimum observed price in EUR/MWh
        max_price: The maximum observed price in EUR/MWh
        ref_price: The reference price in EUR/MWh
        last_hour_price: The last hour price in EUR/MWh
        buy_volume: The buy volume in MWh
        sell_volume: The sell volume in MWh
    """
    zone: str = Field(..., description="Zone identifier")
    first_price: Optional[float] = Field(...,
                                         description="First price in EUR/MWh")
    last_price: Optional[float] = Field(...,
                                        description="Last price in EUR/MWh")
    min_price: Optional[float] = Field(...,
                                       description="Minimum price in EUR/MWh")
    max_price: Optional[float] = Field(...,
                                       description="Maximum price in EUR/MWh")
    ref_price: Optional[float] = Field(...,
                                       description="Reference price in EUR/MWh")
    last_hour_price: Optional[float] = Field(...,
                                             description="Last hour price in EUR/MWh")
    buy_volume: Optional[float] = Field(..., description="Buy volume in MWh")
    sell_volume: Optional[float] = Field(..., description="Sell volume in MWh")


class IpexQuantityResponse(BaseTimeSeriesWithResolutionResponse):
    """Model for IPEX quantity data.
    This model represents the quantity of electricity traded in the IPEX markets.
    Attributes:
        market: The market identifier (e.g., MGP, MI1, MI2)
        zone: The zone identifier (e.g., NORD, CSUD)
        purpose: The purpose of the trade (e.g., BUY, SELL)
        quantity: The quantity of electricity in MWh
    """
    market: str = Field(..., description="Market identifier")
    zone: str = Field(..., description="Zone identifier")
    purpose: str = Field(..., description="BUY or SELL")
    quantity: float = Field(..., description="Quantity in MWh")


class IPEXAncillaryServicesResponse(BaseTimeSeriesWithResolutionResponse):
    """Model for IPEX ancillary services data.
    This model represents the ancillary services market data in IPEX,
    including buy and sell volumes, prices, and market segments.
    Attributes:
        zone: The zone identifier (e.g., NORD, CSUD)
        market: The market identifier (e.g., MSD, MB)
        segment: The market segment (e.g., MSD, MBs, MBa, MB)
        buy_volume: The buy volume in MWh
        sell_volume: The sell volume in MWh
        buy_volume_no_rev: The buy volume without revision in MWh
        sell_volume_no_rev: The sell volume without revision in MWh
        avg_buy_price: The average buy price in EUR/MWh
        avg_sell_price: The average sell price in EUR/MWh
        max_sell_price: The maximum sell price in EUR/MWh
        min_buy_price: The minimum buy price in EUR/MWh
    """
    zone: str = Field(..., description="Zone identifier")
    market: str = Field(..., description="Market identifier (e.g., MSD, MB)")
    segment: str = Field(...,
                         description="Market segment (e.g., MSD, MBs, MBa, MB)")
    buy_volume: Optional[float] = Field(None, description="Buy volume in MWh")
    sell_volume: Optional[float] = Field(
        None, description="Sell volume in MWh")
    buy_volume_no_rev: Optional[float] = Field(
        None, description="Buy volume without revision in MWh")
    sell_volume_no_rev: Optional[float] = Field(
        None, description="Sell volume without revision in MWh")
    avg_buy_price: Optional[float] = Field(
        None, description="Average buy price in EUR/MWh")
    avg_sell_price: Optional[float] = Field(
        None, description="Average sell price in EUR/MWh")
    max_sell_price: Optional[float] = Field(
        None, description="Maximum sell price in EUR/MWh")
    min_buy_price: Optional[float] = Field(
        None, description="Minimum buy price in EUR/MWh")


class IPEXFlowResponse(BaseTimeSeriesWithResolutionResponse):
    """Model for IPEX flow data.
    This model represents the commercial flow of electricity between zones in the IPEX markets.
    Attributes:
        market: The market identifier (e.g., MGP, MI1, MI2)
        zone_from: The zone from which the flow originates
        zone_to: The zone to which the flow is directed
        flow: The flow value in MW
    """

    market: str = Field(...,
                        description="Market identifier (e.g., MGP, MI1, MI2)")
    zone_from: str = Field(..., description="Zone FROM identifier")
    zone_to: str = Field(..., description="Zone TO identifier")
    flow: float = Field(..., description="Flow value in MW")


class IPEXFlowLimitResponse(BaseTimeSeriesWithResolutionResponse):
    """Model for IPEX flow limit data.
    This model represents the flow limits between zones in the IPEX markets.
    Attributes:
        market: The market identifier (e.g., MGP, MI1, MI2)
        zone_from: The zone from which the flow limit originates
        zone_to: The zone to which the flow limit is directed
        flow_limit: The flow limit value in MW
        coefficient: The coefficient value for the flow limit
    """

    market: str = Field(...,
                        description="Market identifier (e.g., MGP, MI1, MI2)")
    zone_from: str = Field(..., description="Zone FROM identifier")
    zone_to: str = Field(..., description="Zone TO identifier")
    flow_limit: float = Field(..., description="Flow value in MW")
    coefficient: float = Field(..., description="Coefficient value")


class IPEXEstimatedDemandResponse(BaseTimeSeriesWithResolutionResponse):
    """Model for IPEX estimated demand data.
    This model represents the estimated demand for electricity in IPEX markets.
    Attributes:
        zone: The zone identifier (e.g., NORD, CSUD)
        demand: The estimated demand value in MW
    """

    zone: str = Field(..., description="Zone identifier")
    demand: float = Field(..., description="Estimated demand value in MW")


class IPEXActualDemandResponse(BaseTimeSeriesWithResolutionResponse):
    """Model for IPEX actual demand data.
    This model represents the actual demand for electricity in IPEX markets.
    Attributes:
        zone: The zone identifier (e.g., NORD, CSUD)
        demand: The actual demand value in MW
    """

    zone: str = Field(..., description="Zone identifier")
    demand: float = Field(..., description="Actual demand value in MW")


class ItalyImbalanceDataResponse(BaseTimeSeriesResponse):
    """Model for Terna imbalance data.
    This model represents the imbalance data for the Italian electricity market,
    including imbalance volume, sign, price, and non-arbitrage price.
    Attributes:
        macrozone: The macrozone identifier (NORD or SUD)
        imb_volume: The imbalance volume in MWh
        imb_sign: The imbalance sign (-1, 0, or 1)
        imb_price: The imbalance price in EUR/MWh
        imb_base_price: The imbalance base price in EUR/MWh
        pnamz: The non-arbitrage price (PNAMZ) in EUR/MWh
        scambi: The scambi value in MW
        estero: The estero value in MW
        is_final_sign: Indicates if the imbalance sign data is final (True) or provisional (False)
        is_final_price: Indicates if the imbalance price data is final (True) or provisional (False)
        is_final_pnamz: Indicates if the non-arbitrage price data is final (True) or provisional (False)
    """

    macrozone: str = Field(...,
                           description="Macrozone identifier (NORD or SUD)")
    imb_volume: Optional[float] = Field(
        None, description="Imbalance volume in MWh")
    imb_sign: Optional[int] = Field(
        None, description="Imbalance sign (-1, 0, or 1)")
    imb_price: Optional[float] = Field(
        None, description="Imbalance price in EUR/MWh")
    imb_base_price: Optional[float] = Field(
        None, description="Imbalance base price in EUR/MWh")
    pnamz: Optional[float] = Field(
        None, description="Non-arbitrage price (PNAMZ) in EUR/MWh")
    scambi: Optional[float] = Field(None, description="Scambi value in MW")
    estero: Optional[float] = Field(None, description="Estero value in MW")
    is_final_sign: Optional[bool] = Field(None,
                                          description="Indicates if the data is final (True) or provisional (False)")
    is_final_price: Optional[bool] = Field(None,
                                           description="Indicates if the price is final (True) or provisional (False)")
    is_final_pnamz: Optional[bool] = Field(None,
                                           description="Indicates if the non-arbitrage price is final (True) or provisional (False)")


class TernaImbalancePriceResponse(BaseTimeSeriesResponse):
    """Model for Terna imbalance price data.
    This model represents the imbalance price data for the Italian electricity market.
    Attributes:
        macrozone: The macrozone identifier (NORD or SUD)
        imb_price: The imbalance price in EUR/MWh
        imb_base_price: The imbalance base price in EUR/MWh
        is_final: Indicates if the price is final (True) or provisional (False)
    """

    macrozone: str = Field(...,
                           description="Macrozone identifier (NORD or SUD)")
    imb_price: Optional[float] = Field(
        None, description="Imbalance price in EUR/MWh")
    imb_base_price: Optional[float] = Field(
        None, description="Imbalance base price in EUR/MWh")
    is_final: Optional[bool] = Field(None,
                                     description="Indicates if the price is final (True) or provisional (False)")


class TernaImbalanceVolumeResponse(BaseTimeSeriesResponse):
    """Model for Terna imbalance volume data.
    This model represents the imbalance volume data for the Italian electricity market.
    Attributes:
        macrozone: The macrozone identifier (NORD or SUD)
        imb_volume: The imbalance volume in MW
        is_final: Indicates if the data is final (True) or provisional (False)
    """

    macrozone: str = Field(...,
                           description="Macrozone identifier (NORD or SUD)")
    imb_volume: Optional[float] = Field(
        None, description="Imbalance volume in MW")
    is_final: Optional[bool] = Field(None,
                                     description="Indicates if the data is final (True) or provisional (False)")


class TernaImbalanceSignResponse(BaseTimeSeriesResponse):
    """Model for Terna imbalance sign data.
    This model represents the imbalance sign data for the Italian electricity market.
    Attributes:
        macrozone: The macrozone identifier (NORD or SUD)
        imb_sign: The imbalance sign (-1, 0, or 1)
        is_final: Indicates if the data is final (True) or provisional (False)
    """

    macrozone: str = Field(...,
                           description="Macrozone identifier (NORD or SUD)")
    imb_sign: Optional[int] = Field(
        None, description="Imbalance sign (-1, 0, or 1)")
    is_final: Optional[bool] = Field(None,
                                     description="Indicates if the data is final (True) or provisional (False)")


class TernaNonArbitragePriceResponse(BaseTimeSeriesResponse):
    """Model for Terna non-arbitrage price data.
    This model represents the non-arbitrage price data for the Italian electricity market.
    Attributes:
        macrozone: The macrozone identifier (NORD or SUD)
        pnamz: The non-arbitrage price (PNAMZ) in EUR/MWh
        time_resolution: The time resolution of the data (e.g., PT60M, PT15M)
        is_final: Indicates if the non-arbitrage price is final (True) or provisional (False)
    """

    macrozone: str = Field(...,
                           description="Macrozone identifier (NORD or SUD)")
    pnamz: Optional[float] = Field(
        None, description="Non-arbitrage price (PNAMZ) in EUR/MWh")
    time_resolution: str = Field(...,
                                 description="Time resolution (PT60M or PT15M)")
    is_final: Optional[bool] = Field(None,
                                     description="Indicates if the non-arbitrage price is final (True) or provisional (False)")


class GenerationData(BaseTimeSeriesResponse):
    """Model for generation data.
    This model represents the generation data for different types of energy sources.
    Attributes:
        area: The area code (e.g., DE, FR, IT)
        gen_type: The type of generation (e.g., WIND, SOLAR, THERMAL)
        data_value: The generation value in MW
    """

    area: str = Field(..., description="Area code")
    gen_type: str = Field(..., description="Generation type")
    data_value: Optional[float] = Field(
        None, description="Generation value in MW")


class LoadData(BaseTimeSeriesResponse):
    """Model for load data.
    This model represents the load data for different areas.
    Attributes:
        area: The area code (e.g., DE, FR, IT)
        data_value: The load value in MW
    """

    area: str = Field(..., description="Area code")
    data_value: Optional[float] = Field(None, description="Load value in MW")


class SpainPriceResponse(BaseTimeSeriesWithResolutionResponse):
    """Model for Spain price data.
    This model represents the price data for the Spanish electricity market.
    Attributes:
        market: The market identifier (e.g., MD, MI1, MI2)
        zone: The zone identifier (e.g., ES, CSUD)
        price: The price value in EUR/MWh
    """

    market: str = Field(...,
                        description="Market identifier (e.g., MD, MI1, MI2)")
    zone: str = Field(..., description="Zone identifier")
    price: float = Field(..., description="Price value in EUR/MWh")


class SpainXbidResultsResponse(BaseTimeSeriesWithResolutionResponse):
    """Model for Spain XBID results data.
    This model represents the results of the cross-border intraday market (XBID) in Spain.
    Attributes:
        zone: The zone identifier (e.g., ES, CSUD)
        wavg_price: The weighted average price value in EUR/MWh
        min_price: The minimum price value in EUR/MWh
        max_price: The maximum price value in EUR/MWh
    """

    zone: str = Field(..., description="Zone identifier")
    wavg_price: Optional[float] = Field(
        None, description="Weighted average price value in EUR/MWh")
    min_price: Optional[float] = Field(
        None, description="Minimum price value in EUR/MWh")
    max_price: Optional[float] = Field(
        None, description="Maximum price value in EUR/MWh")
