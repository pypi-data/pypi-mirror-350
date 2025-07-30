# Add these imports at the top
import os
from datetime import datetime, date
from typing import Dict, Any, Optional, Union, Type, TYPE_CHECKING, TypeVar

import pandas as pd
import requests

from enemera.core.exceptions import ConfigurationError
from enemera.core.response import APIResponse
from enemera.security import validate_api_key, SecureSession, SecureConfig
from enemera.utils.logging import logger

# Keep existing TypeVar
T = TypeVar('T')

if TYPE_CHECKING:
    import polars as pl


class BaseCurveClient:
    """Enhanced base class with security features and backward compatibility"""

    def __init__(self, base_url: str,
                 api_key: Optional[str] = None,
                 use_secure_session: bool = True):
        """
        Initialize base client with optional security enhancements
        
        Args:
            base_url: API base URL
            api_key: API key (if None, attempts to load from environment)
            use_secure_session: Whether to use enhanced security features
        """
        self.base_url = base_url.rstrip('/')
        self.use_secure_session = use_secure_session

        if use_secure_session:
            self._init_secure_session(api_key)
        else:
            self._init_legacy_session(api_key)

    def _init_secure_session(self, api_key: Optional[str] = None):
        """Initialize with enhanced security"""

        # Load configuration securely
        if api_key is None:
            try:
                config = SecureConfig.load_from_env()
                api_key = config.get('api_key')
            except Exception as e:
                logger.debug(f"Could not load secure config: {e}")
                api_key = os.getenv('ENEMERA_API_KEY')

        if api_key is None:
            raise ConfigurationError(
                "API key required. Set ENEMERA_API_KEY environment variable "
                "or pass api_key parameter"
            )

        # Validate API key
        validated_key = validate_api_key(api_key)

        # Initialize secure session
        self.secure_session = SecureSession(validated_key, self.base_url)
        self.session = self.secure_session.session  # For backward compatibility

    def _init_legacy_session(self, api_key: Optional[str] = None):
        """Initialize with legacy session (for backward compatibility)"""

        self.session = requests.Session()

        # Get API key from environment if not provided
        if api_key is None:
            api_key = os.getenv('ENEMERA_API_KEY')

        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> requests.Response:
        """Make HTTP request with enhanced error handling"""

        # Format parameters (keep existing logic)
        formatted_params = {}
        date_from = None
        date_to = None

        for key, value in params.items():
            if value is not None:
                if key in ['date_from', 'date_to']:
                    try:
                        formatted_value = self._format_date(value)
                        datetime.strptime(formatted_value, '%Y-%m-%d')
                        formatted_params[key] = formatted_value

                        if key == 'date_from':
                            date_from = formatted_value
                        elif key == 'date_to':
                            date_to = formatted_value

                    except ValueError:
                        raise ValueError(f"Invalid date format for {key}: {value}")
                else:
                    formatted_params[key] = value

        # Validate date range
        if date_from and date_to:
            from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
            to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
            if to_date < from_date:
                raise ValueError(f"date_to ({date_to}) cannot be before date_from ({date_from})")

        # Make request using appropriate session
        url = f"{self.base_url}{endpoint}"

        if self.use_secure_session and hasattr(self, 'secure_session'):
            return self.secure_session.make_request('GET', url, params=formatted_params)
        else:
            response = self.session.get(url, params=formatted_params)
            response.raise_for_status()
            return response

    # Keep existing methods unchanged
    @staticmethod
    def _format_date(date_obj: Union[str, datetime, date]) -> str:
        """Format date for API request"""
        if isinstance(date_obj, str):
            return date_obj
        elif isinstance(date_obj, datetime):
            return date_obj.strftime('%Y-%m-%d')
        elif isinstance(date_obj, date):
            return date_obj.strftime('%Y-%m-%d')
        else:
            return str(date_obj)

    @staticmethod
    def _parse_response(response: requests.Response, model_class: Type[T]) -> APIResponse[T]:
        """Parse response into model objects"""
        data = response.json()
        items = [model_class(**item) for item in data]
        return APIResponse(items)

    def get_pandas(self, **kwargs) -> pd.DataFrame:
        """Get data as pandas DataFrame"""
        return self.get(**kwargs).to_pandas()

    def get_polars(self, **kwargs) -> 'pl.DataFrame':
        """Get data as polars DataFrame"""
        return self.get(**kwargs).to_polars()
