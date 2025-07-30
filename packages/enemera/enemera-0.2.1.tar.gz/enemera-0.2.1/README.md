# Enemera API Client

[![PyPI version](https://badge.fury.io/py/enemera.svg)](https://badge.fury.io/py/enemera)
[![Python](https://img.shields.io/pypi/pyversions/enemera.svg)](https://pypi.org/project/enemera/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python client for the Enemera energy data API, providing secure access to European electricity market data with enhanced functionality, robust security features, and type-safe interfaces.

## Key Features

- **🔐 Enhanced Security**: JWT token validation, secure session management, and credential protection
- **📊 Multiple Output Formats**: Native support for pandas DataFrames, Polars DataFrames, CSV, and Excel exports
- **🔒 Type Safety**: Comprehensive enums for markets, areas, and trading purposes with validation
- **🌍 Timezone Handling**: Automatic UTC to CET timezone conversion for European energy markets
- **⚡ Robust Error Handling**: Detailed exception hierarchy with retry logic and rate limiting
- **🎯 Flexible Data Access**: Generic curve access via unified client or specialized country-specific clients
- **📦 Optional Dependencies**: Install only what you need for your specific use case
- **🛡️ Secure by Default**: Built-in API key validation and secure HTTP session management
- **📅 Smart Period Calculation**: Automatic delivery date and period calculation following IPEX/OMIE conventions
- **🔄 Long Period Downloads**: Built-in chunking for downloading extended time series data

## Supported Markets

### Italy (IPEX)

- **Prices**: Day-ahead (MGP) and intraday markets (MI1-MI7)
- **XBID Results**: Cross-border intraday trading data with price statistics
- **Exchange Volumes**: Trading volumes by market and purpose (BUY/SELL)
- **Ancillary Services**: MSD, MB, MBa, MBs market data with detailed metrics
- **Load Data**: Actual and forecast consumption by bidding zone
- **Generation**: Actual and forecast generation by technology type
- **Commercial Flows**: Inter-zonal power flows and capacity limits
- **Imbalance Data**: System imbalance volumes, prices, and settlement data (PT15M and PT60M)
- **DAM Demand**: Day-ahead market actual and forecasted demand

### Spain (OMIE)

- **Prices**: Day-ahead (MD) and intraday market prices
- **XBID Results**: Cross-border intraday trading data

## Installation

### Basic Installation

```bash
pip install enemera
```

### With Optional Dependencies

```bash
# For pandas support
pip install enemera[pandas]

# For polars support  
pip install enemera[polars]

# For Excel export with openpyxl
pip install enemera[excel]

# For Excel export with xlsxwriter
pip install enemera[excel-xlsxwriter]

# Install everything
pip install enemera[all]

# Development dependencies
pip install enemera[dev]
```

## Quick Start

### Authentication

The client supports JWT-based API key authentication with built-in validation:

```python
from enemera import EnemeraClient

# Initialize with API key (recommended)
client = EnemeraClient(api_key="your-jwt-api-key")

# Or set via environment variable ENEMERA_API_KEY
import os
os.environ['ENEMERA_API_KEY'] = "your-jwt-api-key"
client = EnemeraClient()
```

### Basic Usage

```python
from enemera import EnemeraClient, Curve
from datetime import date

client = EnemeraClient(api_key="your-jwt-api-key")

# Get Italian day-ahead prices
response = client.get(
    curve=Curve.ITALY_PRICES,
    market="MGP",
    date_from=date(2024, 1, 1),
    date_to=date(2024, 1, 7),
    area="NORD"
)

# Convert to pandas DataFrame
df = response.to_pandas()
print(df.head())
```

### Using Type-Safe Enums

```python
from enemera import EnemeraClient, Curve, Market, Area, Purpose

client = EnemeraClient(api_key="your-jwt-api-key")

# Type-safe market and area specification
response = client.get(
    curve=Curve.ITALY_PRICES,
    market=Market.MGP,
    area=Area.NORD,
    date_from="2024-01-01",
    date_to="2024-01-07"
)
```

### Direct DataFrame Access

```python
# Get data directly as pandas DataFrame with UTC timestamps
df = client.get_pandas(
    curve=Curve.ITALY_PRICES,
    market=Market.MGP,
    area=Area.NORD,
    date_from="2024-01-01",
    date_to="2024-01-07"
)

# Get data with CET timezone conversion
df_cet = client.get_pandas_cet(
    curve=Curve.ITALY_LOAD_ACTUAL,
    date_from="2024-01-01",
    date_to="2024-01-07",
    area=Area.NORD
)
```

## Advanced Features

### Delivery Period Calculation

The client includes sophisticated utility functions for energy market conventions:

```python
from enemera.utils.utility_functions import calc_delivery_period
import pandas as pd

# Get price data
df = client.get_pandas_cet(
    curve=Curve.ITALY_PRICES,
    market=Market.MGP,
    area=Area.NORD,
    date_from="2024-01-01",
    date_to="2024-01-07"
)

# Calculate delivery date and period according to IPEX/OMIE conventions
# Handles DST changes automatically
df_with_periods = calc_delivery_period(df)

print(df_with_periods[['delivery_date', 'period', 'price']].head())
```

**Period Calculation Rules:**
- **60-minute resolution (PT60M)**: Periods 1-24 (25 periods on DST change days)
- **15-minute resolution (PT15M)**: Periods 1-96 (100 periods on DST change days)
- **DST Handling**: Automatically accounts for the last Sunday in October transitions
- **CET-based**: All calculations use Central European Time as reference

### Long Period Downloads

For extended time series, use the built-in chunking utility:

```python
from enemera.utils.utility_functions import download_long_period
from datetime import date

# Download a full year of data in manageable chunks
df_year = download_long_period(
    client=client,
    curve=Curve.ITALY_PRICES,
    start_date=date(2023, 1, 1),
    end_date=date(2023, 12, 31),
    step_days=30,  # Download in 30-day chunks
    market=Market.MGP,
    area=Area.NORD
)

print(f"Downloaded {len(df_year)} data points covering {df_year.index.min()} to {df_year.index.max()}")
```

### Time Resolution Support

Many endpoints now include time resolution information:

```python
# Get 15-minute imbalance data
imbalance_15m = client.get(
    curve=Curve.ITALY_IMBALANCE_DATA,
    date_from="2024-01-01",
    date_to="2024-01-07",
    area="NORD"
)

# Get legacy 60-minute imbalance data
imbalance_60m = client.get(
    curve=Curve.ITALY_IMBALANCE_DATA_PT60M,
    date_from="2024-01-01",
    date_to="2024-01-07",
    area="NORD"
)

# Check time resolution in the data
df = imbalance_15m.to_pandas()
print(df['time_resolution'].unique())  # ['PT15M']
```

## Security Features

### JWT Token Validation

The client automatically validates JWT tokens with comprehensive checks:

```python
from enemera.security import validate_api_key, get_token_info

# Validate API key format and content
try:
    validated_key = validate_api_key("your-jwt-token")
    print("API key is valid")
    
    # Get token information (for debugging)
    token_info = get_token_info(validated_key)
    print(f"Token expires at: {token_info['expires_at']}")
    
except AuthenticationError as e:
    print(f"Invalid API key: {e}")
```

### Secure Session Management

```python
# Enable secure session (default)
client = EnemeraClient(api_key="your-key", use_secure_session=True)

# Legacy mode (for backward compatibility)
client = EnemeraClient(api_key="your-key", use_secure_session=False)
```

## Data Export

### CSV Export

```python
response = client.get(curve=Curve.ITALY_PRICES, market="MGP", ...)
response.to_csv("prices.csv", index=True)
```

### Excel Export

```python
response = client.get(curve=Curve.ITALY_PRICES, market="MGP", ...)
response.to_excel("prices.xlsx", sheet_name="Prices", index=True)
```

### Polars DataFrame

```python
response = client.get(curve=Curve.ITALY_PRICES, market="MGP", ...)
df_polars = response.to_polars()
```

## Country-Specific Clients

For specialized access, use dedicated client classes:

### Italy Clients

```python
from enemera.api import (
    ItalyPricesClient, 
    ItalyLoadActualClient, 
    ItalyGenerationClient,
    ItalyImbalanceDataClient,
    ItalyXbidResultsClient
)

# Italian electricity prices
italy_prices = ItalyPricesClient(api_key="your-key")
prices = italy_prices.get(
    market="MGP",
    date_from="2024-01-01",
    date_to="2024-01-07",
    area="NORD"
)

# Load data
italy_load = ItalyLoadActualClient(api_key="your-key")
load_data = italy_load.get(
    date_from="2024-01-01",
    date_to="2024-01-07",
    area="NORD"
)

# Generation data by technology
italy_gen = ItalyGenerationClient(api_key="your-key")
generation = italy_gen.get(
    generation_type="WIND",
    date_from="2024-01-01",
    date_to="2024-01-07",
    area="NORD"
)

# Imbalance data (15-minute resolution)
italy_imb = ItalyImbalanceDataClient(api_key="your-key")
imbalance = italy_imb.get(
    date_from="2024-01-01",
    date_to="2024-01-07",
    area="NORD"
)

# Legacy imbalance data (60-minute resolution)
from enemera.api import ItalyImbalanceDataPT60MClient
italy_imb_60m = ItalyImbalanceDataPT60MClient(api_key="your-key")
imbalance_60m = italy_imb_60m.get(
    date_from="2024-01-01",
    date_to="2024-01-07",
    area="NORD"
)
```

### Spain Clients

```python
from enemera.api import SpainPricesClient, SpainXbidResultsClient

# Spanish electricity prices
spain_prices = SpainPricesClient(api_key="your-key")
prices = spain_prices.get(
    market="MD",
    date_from="2024-01-01",
    date_to="2024-01-07"
)

# Spanish XBID results
spain_xbid = SpainXbidResultsClient(api_key="your-key")
xbid_data = spain_xbid.get(
    date_from="2024-01-01",
    date_to="2024-01-07"
)
```

## Available Data Curves

| Curve                         | Description                        | Parameters                    | Time Resolution |
|-------------------------------|------------------------------------|-------------------------------|-----------------|
| `ITALY_PRICES`                | Day-ahead and intraday prices     | market, area                  | PT60M/PT15M     |
| `ITALY_XBID_RESULTS`          | Cross-border intraday results     | area                          | PT60M/PT15M     |
| `ITALY_EXCHANGE_VOLUMES`      | Trading volumes by purpose        | market, area, purpose         | PT60M/PT15M     |
| `ITALY_ANCILLARY_SERVICES`    | Ancillary services market data    | market, market_segment, area  | PT60M/PT15M     |
| `ITALY_DAM_DEMAND_ACT`        | Actual day-ahead demand           | area                          | PT60M/PT15M     |
| `ITALY_DAM_DEMAND_FCS`        | Forecasted day-ahead demand       | area                          | PT60M/PT15M     |
| `ITALY_LOAD_ACTUAL`           | Actual electricity consumption    | area                          | PT60M           |
| `ITALY_LOAD_FORECAST`         | Forecasted consumption            | area                          | PT60M           |
| `ITALY_GENERATION`            | Actual generation by technology   | generation_type, area         | PT60M           |
| `ITALY_GENERATION_FORECAST`   | Forecasted generation             | generation_type, area         | PT60M           |
| `ITALY_COMMERCIAL_FLOWS`      | Inter-zonal power flows           | market, area_from, area_to    | PT60M/PT15M     |
| `ITALY_COMMERCIAL_FLOW_LIMITS`| Flow capacity limits              | market, area_from, area_to    | PT60M/PT15M     |
| `ITALY_IMBALANCE_DATA`        | System imbalance data (15-min)    | area                          | PT15M           |
| `ITALY_IMBALANCE_DATA_PT60M`  | System imbalance data (60-min)    | area                          | PT60M           |
| `SPAIN_PRICES`                | Day-ahead and intraday prices     | market                        | PT60M/PT15M     |
| `SPAIN_XBID_RESULTS`          | Cross-border intraday results     | -                             | PT60M/PT15M     |

## Enums Reference

### Markets

```python
from enemera import Market

# Italian markets
Market.MGP    # Day-Ahead Market (Mercato del Giorno Prima)
Market.MI1    # Intraday Market 1
Market.MI2    # Intraday Market 2
Market.MI3    # Intraday Market 3
Market.MI4    # Intraday Market 4
Market.MI5    # Intraday Market 5
Market.MI6    # Intraday Market 6
Market.MI7    # Intraday Market 7
Market.MSD    # Ancillary Services Market
Market.MB     # Balancing Market
Market.MBa    # Balancing Market - altri servizi
Market.MBs    # Balancing Market - secondary reserve
```

### Areas (Italy)

```python
from enemera import Area

# Primary bidding zones
Area.NORD     # North zone
Area.CNOR     # Center-North zone
Area.CSUD     # Center-South zone
Area.SUD      # South zone
Area.SICI     # Sicily
Area.SARD     # Sardinia
Area.CALA     # Calabria

# Macrozones (for imbalance pricing)
Area.NORTH    # North macrozone (alias for NORD)
Area.SOUTH    # South macrozone

# Virtual zones
Area.BRNN     # Brindisi
Area.FOGN     # Foggia
Area.MONT     # Montalto
Area.PRGP     # Priolo Gargallo
Area.ROSN     # Rossano

# Foreign virtual zones
Area.AUST     # Austria
Area.CORS     # Corsica
Area.COAC     # Corsica AC
Area.COAD     # Corsica DC
Area.FRAN     # France
Area.GREC     # Greece
Area.SLOV     # Slovenia
Area.SVIZ     # Switzerland
Area.MALT     # Malta
```

### Trading Purpose

```python
from enemera import Purpose

Purpose.BUY   # Buy orders/volumes
Purpose.SELL  # Sell orders/volumes
```

## Error Handling

The client provides comprehensive error handling with detailed exception types:

```python
from enemera import (
    EnemeraClient,
    AuthenticationError,
    RateLimitError,
    APIError,
    ValidationError,
    ConnectionError,
    TimeoutError,
    DependencyError
)

client = EnemeraClient(api_key="your-key")

try:
    response = client.get(curve=Curve.ITALY_PRICES, market="MGP", ...)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except APIError as e:
    print(f"API error {e.status_code}: {e.detail}")
except ConnectionError as e:
    print(f"Connection failed: {e}")
except DependencyError as e:
    print(f"Missing dependency: {e.install_command}")
```

## Configuration

### Environment Variables

```bash
export ENEMERA_API_KEY="your-jwt-api-key"
export ENEMERA_BASE_URL="https://api.enemera.com"  # Optional, defaults to official API
export ENEMERA_TIMEOUT="30"  # Optional, request timeout in seconds
```

### Logging Configuration

```python
from enemera.utils.logging import configure_logging, get_logger

# Configure global logging level
configure_logging(level="debug")

# Get a custom logger for your application
logger = get_logger("my_energy_app", level="info")
logger.info("Starting energy data analysis")
```

## Advanced Usage

### Date Handling

```python
from datetime import datetime, date

# Multiple date formats supported
client.get(
    curve=Curve.ITALY_PRICES,
    market="MGP",
    date_from="2024-01-01",        # ISO string
    date_to=date(2024, 1, 7),      # Date object
    # date_to=datetime(2024, 1, 7), # Datetime object
    area="NORD"
)
```

### Timezone Conversion

```python
# Get data with UTC timestamps (default)
df_utc = response.to_pandas()

# Get data with CET timestamps (common for European energy markets)
df_cet = response.to_pandas_cet()

# Get naive datetime (no timezone info) - useful for Excel export
df_naive = response.to_pandas(naive_datetime=True)
```

### Working with Exchange Volumes

```python
from enemera import Purpose

# Get buy volumes for MGP market
buy_volumes = client.get(
    curve=Curve.ITALY_EXCHANGE_VOLUMES,
    market=Market.MGP,
    purpose=Purpose.BUY,
    date_from="2024-01-01",
    date_to="2024-01-07",
    area=Area.NORD
)

# Get all volumes (both buy and sell)
all_volumes = client.get(
    curve=Curve.ITALY_EXCHANGE_VOLUMES,
    market=Market.MGP,
    date_from="2024-01-01",
    date_to="2024-01-07",
    area=Area.NORD
)
```

### Working with Generation Data

```python
# Get wind generation data
wind_gen = client.get(
    curve=Curve.ITALY_GENERATION,
    generation_type="WIND",
    date_from="2024-01-01",
    date_to="2024-01-07",
    area=Area.NORD
)

# Get solar generation forecast
solar_forecast = client.get(
    curve=Curve.ITALY_GENERATION_FORECAST,
    generation_type="SOLAR",
    date_from="2024-01-01",
    date_to="2024-01-07",
    area=Area.NORD
)
```

### Working with Commercial Flows

```python
# Get flows between specific zones
flows = client.get(
    curve=Curve.ITALY_COMMERCIAL_FLOWS,
    market=Market.MGP,
    area_from=Area.NORD,
    area_to=Area.CNOR,
    date_from="2024-01-01",
    date_to="2024-01-07"
)

# Get flow limits
flow_limits = client.get(
    curve=Curve.ITALY_COMMERCIAL_FLOW_LIMITS,
    market=Market.MGP,
    area_from=Area.NORD,
    area_to=Area.CNOR,
    date_from="2024-01-01",
    date_to="2024-01-07"
)
```

### Working with Imbalance Data

```python
# Get current 15-minute imbalance data
imbalance_15m = client.get(
    curve=Curve.ITALY_IMBALANCE_DATA,
    date_from="2024-01-01",
    date_to="2024-01-07",
    area="NORD"
)

# Get legacy 60-minute imbalance data
imbalance_60m = client.get(
    curve=Curve.ITALY_IMBALANCE_DATA_PT60M,
    date_from="2024-01-01",
    date_to="2024-01-07",
    area="NORD"
)

# Convert to DataFrame and calculate delivery periods
df_imb = imbalance_15m.to_pandas_cet()
df_with_periods = calc_delivery_period(df_imb)

print(df_with_periods[['delivery_date', 'period', 'imb_price', 'imb_volume']].head())
```

## Data Models and Response Structure

### Time Resolution

Many responses now include time resolution information:

```python
# Check what time resolution is available
df = response.to_pandas()
print(df['time_resolution'].unique())  # ['PT60M'] or ['PT15M']
```

### Enhanced Response Models

The client returns structured response objects with the following key models:

- **PriceData**: Electricity prices with market, zone, price, and time resolution
- **IPEXXbidRecapResponse**: XBID trading statistics with price ranges, volumes, and resolution
- **IpexQuantityResponse**: Exchange volumes by market, zone, purpose, and resolution
- **IPEXAncillaryServicesResponse**: Ancillary services market data with resolution
- **GenerationData**: Generation data by area and technology type
- **LoadData**: Load data by area
- **ItalyImbalanceDataResponse**: Comprehensive imbalance data with prices, volumes, and finality flags
- **IPEXFlowResponse**: Commercial flows between bidding zones with resolution
- **SpainPriceResponse**: Spanish market prices with resolution
- **SpainXbidResultsResponse**: Spanish XBID trading results with resolution

All models inherit from `BaseTimeSeriesResponse` or `BaseTimeSeriesWithResolutionResponse` and include UTC timestamps.

### Imbalance Data Structure

```python
# Imbalance data includes comprehensive information
imbalance_df = client.get_pandas(curve=Curve.ITALY_IMBALANCE_DATA, ...)
print(imbalance_df.columns)
# ['macrozone', 'imb_volume', 'imb_sign', 'imb_price', 'imb_base_price', 
#  'pnamz', 'scambi', 'estero', 'is_final_sign', 'is_final_price', 'is_final_pnamz']
```

## Requirements

### Core Dependencies

- Python ≥ 3.7
- requests ≥ 2.25.0
- pydantic ≥ 2.0.0
- python-dateutil ≥ 2.8.0

### Optional Dependencies

- **pandas** ≥ 1.0.0 (for DataFrame support and utility functions)
- **polars** ≥ 0.7.0 (for Polars DataFrame support)
- **openpyxl** ≥ 3.0.0 (for Excel export with .xlsx format)
- **xlsxwriter** ≥ 3.0.0 (alternative Excel writer with advanced formatting)
- **numpy** (for period calculations)
- **pytz** (for timezone handling)

## API Documentation

For detailed API documentation, available endpoints, and data schemas, visit the [Enemera API documentation](https://api.enemera.com/docs).

## Migration Guide

### From v0.1.x to v0.2.0

1. **API Key Format**: Ensure you're using JWT tokens instead of simple API keys
2. **Security Features**: The client now validates JWT tokens by default
3. **New Clients**: Several new specialized clients have been added for different data types
4. **Enhanced Error Handling**: More specific exception types are now available
5. **Time Resolution**: Many responses now include time_resolution field
6. **Utility Functions**: New functions for period calculation and long downloads

### From v0.2.0 to v0.2.1

1. **Utility Functions**: Added `calc_delivery_period()` and `download_long_period()`
2. **Time Resolution Support**: Enhanced response models with time resolution information
3. **Imbalance Data**: New PT60M endpoint for legacy 60-minute data
4. **Period Calculations**: Automatic handling of DST changes in European markets

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
git clone https://github.com/fracasamax/enemera-api-client.git
cd enemera-api-client
pip install -e .[dev]
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black enemera/
isort enemera/
flake8 enemera/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/fracasamax/enemera-api-client/issues)
- **Email**: [dev@elnc.eu](mailto:dev@elnc.eu)
- **Documentation**: [API docs](https://api.enemera.com/docs)

## Changelog

### v0.2.1 - Enhanced Market Utilities & Time Resolution Support

- ✅ **Smart Period Calculation**: Added `calc_delivery_period()` function with IPEX/OMIE convention support
- ✅ **Long Period Downloads**: Added `download_long_period()` for efficient chunked data retrieval
- ✅ **Enhanced Time Resolution**: Added time_resolution field to response models (PT60M/PT15M)
- ✅ **Imbalance Data Improvements**: Separate endpoints for 15-minute and 60-minute historical data
- ✅ **DST Handling**: Automatic Daylight Saving Time handling in period calculations
- ✅ **Enhanced Response Models**: Updated models with comprehensive time resolution support

### v0.2.0 - Enhanced Security & Functionality

- ✅ **Enhanced Security**: JWT token validation and secure session management
- ✅ **New Clients**: Added specialized clients for generation, load, flows, and imbalance data
- ✅ **Improved Error Handling**: Comprehensive exception hierarchy with detailed error information
- ✅ **Better Type Safety**: Enhanced enum validation and parameter checking
- ✅ **Advanced Logging**: Structured logging with credential protection
- ✅ **Configuration Management**: Secure configuration loading from environment and files
- ✅ **Timezone Utilities**: Enhanced timezone handling for European energy markets
- ✅ **Response Models**: Detailed response models for all data types
- ✅ **Optional Dependencies**: Flexible installation with optional features

### v0.1.x - Initial Release

- Basic API client functionality
- Core data access for Italian and Spanish markets
- DataFrame export capabilities

---

**Disclaimer**: This is an unofficial client library. Enemera and associated trademarks are property of their respective owners.