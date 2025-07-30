import logging
import re

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from enemera.core.exceptions import AuthenticationError, RateLimitError, APIError
from enemera.security.validators import validate_api_key


class SecureSession:
    """Secure session management with API key protection"""

    def __init__(self, api_key: str, base_url: str):
        self.session = requests.Session()
        self._setup_security(api_key, base_url)
        self._setup_logging()

    def _setup_security(self, api_key: str, base_url: str):
        """Configure secure session settings"""

        # Validate API key
        validated_key = validate_api_key(api_key)

        # Set headers securely
        self.session.headers.update({
            "Authorization": f"Bearer {validated_key}",
            "Content-Type": "application/json",
        })

        # Configure SSL verification
        self.session.verify = True

        # Configure timeouts
        self.session.timeout = (10, 30)  # (connect, read)

        # Configure retries with backoff
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _setup_logging(self):
        """Configure secure logging that doesn't expose credentials"""

        # Custom log filter to remove sensitive data
        class SensitiveDataFilter(logging.Filter):
            def filter(self, record):
                if hasattr(record, 'msg'):
                    # Remove API keys from log messages
                    record.msg = re.sub(
                        r'Bearer [a-zA-Z0-9-_]{20,}',
                        'Bearer ***REDACTED***',
                        str(record.msg)
                    )
                return True

        # Apply filter to requests logger
        requests_logger = logging.getLogger('requests')
        requests_logger.addFilter(SensitiveDataFilter())

        # Apply filter to urllib3 logger
        urllib3_logger = logging.getLogger('urllib3')
        urllib3_logger.addFilter(SensitiveDataFilter())

    def make_request(self, method: str, url: str, **kwargs):
        """Make secure HTTP request with error handling"""
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response

        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")

        except requests.exceptions.SSLError:
            raise ConnectionError("SSL verification failed")

        except requests.exceptions.ConnectionError:
            raise ConnectionError("Failed to connect to API")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid API key or unauthorized access")
            elif e.response.status_code == 403:
                raise AuthenticationError("API key does not have required permissions")
            elif e.response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            else:
                raise APIError(e.response.status_code, str(e))
