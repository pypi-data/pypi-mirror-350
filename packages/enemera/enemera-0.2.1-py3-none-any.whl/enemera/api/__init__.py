# enemera/api/__init__.py

# Italy clients
from enemera.api.italy.ancillary_services import ItalyAncillaryServicesResultsClient
from enemera.api.italy.dam_demand import ItalyActDamDemandClient, ItalyFcsDamDemandClient
from enemera.api.italy.exchange_volumes import ItalyExchangeVolumesClient
from enemera.api.italy.flows import ItalyCommercialFlowsClient, ItalyCommercialFlowLimitsClient
from enemera.api.italy.generation import ItalyGenerationClient, ItalyGenerationForecastClient
from enemera.api.italy.imbalance import ItalyImbalanceDataClient, ItalyImbalanceDataPT60MClient
from enemera.api.italy.load import ItalyLoadActualClient, ItalyLoadForecastClient
from enemera.api.italy.prices import ItalyPricesClient
from enemera.api.italy.xbid import ItalyXbidResultsClient

# Spain clients
from enemera.api.spain.prices import SpainPricesClient
from enemera.api.spain.xbid import SpainXbidResultsClient

# Export all client classes
__all__ = [
    'ItalyPricesClient',
    'ItalyXbidResultsClient',
    'ItalyAncillaryServicesResultsClient',
    'ItalyActDamDemandClient',
    'ItalyFcsDamDemandClient',
    'ItalyCommercialFlowsClient',
    'ItalyCommercialFlowLimitsClient',
    'ItalyLoadActualClient',
    'ItalyLoadForecastClient',
    'ItalyGenerationClient',
    'ItalyGenerationForecastClient',
    'ItalyImbalanceDataClient',
    'ItalyImbalanceDataPT60MClient',
    'ItalyExchangeVolumesClient',
    'SpainPricesClient',
    'SpainXbidResultsClient'
]
