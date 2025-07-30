"""
Enemera API Client - A Python client for the Enemera energy data API.
"""

__version__ = "0.2.1"

# Import exceptions first as they don't have dependencies
from enemera.core.exceptions import (
    EnemeraError,
    AuthenticationError,
    RateLimitError,
    APIError,
    ValidationError,
    ConnectionError,
    DependencyError
)
from enemera.models.curves import Curve
# Import common enums and models that don't have dependencies
from enemera.models.enums import Market, Area, Purpose
from enemera.utils.utility_functions import calc_delivery_period, download_long_period

# Import response module with optional dependencies
try:
    from enemera.core.response import APIResponse
    # from enemera.data_utils import to_pandas, to_polars, to_csv, to_excel, convert_timezone, to_cet
except ImportError as e:
    # Provide a helpful message if dependencies are missing
    missing_dep = str(e).split("'")[-2] if "'" in str(e) else str(e)
    if "polars" in missing_dep or "pytz" in missing_dep:
        print(
            f"Optional dependency missing: {missing_dep}. Install with 'pip install enemera[polars]'")
    else:
        print(f"Error importing data conversion modules: {e}")

# Import the client and API base which depend on the above
from enemera.api.base import BaseCurveClient
from enemera.client import EnemeraClient

__all__ = [
    "EnemeraClient",
    "Market",
    "Area",
    "Purpose",
    "APIResponse",
    "Curve",
    "calc_delivery_period",
    "download_long_period"
]
