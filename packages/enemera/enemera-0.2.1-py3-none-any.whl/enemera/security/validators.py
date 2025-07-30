"""
Corrected JWT-based API Key Validator for Enemera API
Handles JWT tokens used as API keys
"""

import base64
import json
import os
import re
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from enemera.core.exceptions import AuthenticationError, ConfigurationError


class APIKeyValidator:
    """Validator for JWT-based API keys used by Enemera API"""

    # JWT pattern: header.payload.signature (base64url encoded parts separated by dots)
    JWT_PATTERN = r'^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$'

    MIN_LENGTH = 150  # Based on your example (211 chars), set reasonable minimum
    MAX_LENGTH = 2048  # Reasonable upper limit for JWT tokens

    # Expected token structure based on Enemera API
    EXPECTED_ALGORITHM = "HS256"
    EXPECTED_TYPE = "JWT"
    EXPECTED_TOKEN_TYPE = "api_key"

    @classmethod
    def validate_jwt_format(cls, token: str) -> bool:
        """Validate JWT token format"""
        if not isinstance(token, str):
            return False

        if not (cls.MIN_LENGTH <= len(token) <= cls.MAX_LENGTH):
            return False

        # Check JWT pattern (three base64url parts separated by dots)
        if not re.match(cls.JWT_PATTERN, token):
            return False

        # Verify it has exactly 3 parts
        parts = token.split('.')
        return len(parts) == 3

    @classmethod
    def decode_jwt_header(cls, token: str) -> Optional[Dict[str, Any]]:
        """Decode JWT header for validation"""
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None

            # Decode header (first part)
            header_encoded = parts[0]

            # Add padding if needed
            padding = 4 - (len(header_encoded) % 4)
            if padding != 4:
                header_encoded += '=' * padding

            header_bytes = base64.urlsafe_b64decode(header_encoded)
            header = json.loads(header_bytes.decode('utf-8'))

            return header

        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            return None

    @classmethod
    def validate_jwt_header(cls, header: Dict[str, Any]) -> None:
        """Validate JWT header contains expected values"""

        if header.get('typ') != cls.EXPECTED_TYPE:
            raise AuthenticationError(f"Invalid JWT type: {header.get('typ')}. Expected '{cls.EXPECTED_TYPE}'")

        if header.get('alg') != cls.EXPECTED_ALGORITHM:
            raise AuthenticationError(
                f"Invalid JWT algorithm: {header.get('alg')}. Expected '{cls.EXPECTED_ALGORITHM}'")

    @classmethod
    def decode_jwt_payload(cls, token: str) -> Optional[Dict[str, Any]]:
        """
        Decode JWT payload without verification (for validation purposes only)

        Returns:
            Dict containing payload data or None if invalid
        """
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None

            # Decode payload (second part)
            payload_encoded = parts[1]

            # Add padding if needed (base64url decoding)
            padding = 4 - (len(payload_encoded) % 4)
            if padding != 4:
                payload_encoded += '=' * padding

            # Decode base64
            payload_bytes = base64.urlsafe_b64decode(payload_encoded)
            payload = json.loads(payload_bytes.decode('utf-8'))

            return payload

        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            return None

    @classmethod
    def validate_jwt_payload(cls, payload: Dict[str, Any]) -> None:
        """Validate JWT payload contains expected fields"""

        # Check for required JWT claims
        if 'iat' not in payload:
            raise AuthenticationError("JWT token missing 'iat' (issued at) claim")

        if 'exp' not in payload:
            raise AuthenticationError("JWT token missing 'exp' (expiration) claim")

        # Check if token is expired
        current_time = datetime.now(timezone.utc).timestamp()
        if payload['exp'] < current_time:
            raise AuthenticationError("JWT token has expired")

        # Check for Enemera-specific claims (based on your example)
        if 'type' in payload and payload['type'] != cls.EXPECTED_TOKEN_TYPE:
            raise AuthenticationError(f"Invalid token type: {payload['type']}. Expected '{cls.EXPECTED_TOKEN_TYPE}'")

        # Validate issued at time is reasonable (not too far in future)
        if payload['iat'] > current_time + 300:  # 5 minute tolerance
            raise AuthenticationError("JWT token issued in the future")

    @classmethod
    def validate_security(cls, token: str) -> None:
        """Perform security validation on JWT token"""

        # Check for obviously fake or test tokens
        if token.lower().startswith(('test', 'demo', 'example', 'fake')):
            raise AuthenticationError("Token appears to be a test/demo token")

        # Check signature part isn't empty or obviously invalid
        parts = token.split('.')
        signature = parts[2]

        if len(signature) < 10:  # Signature should be substantial
            raise AuthenticationError("JWT signature appears to be invalid")

        # Basic entropy check on signature
        unique_chars = len(set(signature.lower()))
        if unique_chars < 8:  # Should have reasonable character variety
            raise AuthenticationError("JWT signature has insufficient entropy")


def validate_api_key(api_key: Optional[str] = None) -> str:
    """
    Comprehensive JWT API key validation for Enemera API

    Args:
        api_key: JWT token string or None to check environment

    Returns:
        str: Validated JWT token

    Raises:
        AuthenticationError: If API key is invalid or missing
        ConfigurationError: If environment setup is incorrect
    """

    # 1. Resolve API key source
    if api_key is None:
        api_key = os.getenv('ENEMERA_API_KEY')

        if api_key is None:
            raise ConfigurationError(
                "API key not provided. Set ENEMERA_API_KEY environment variable "
                "or pass api_key parameter"
            )

    # 2. Basic validation
    if not api_key or not isinstance(api_key, str):
        raise AuthenticationError("API key must be a non-empty string")

    # Remove whitespace
    api_key = api_key.strip()

    if not api_key:
        raise AuthenticationError("API key cannot be empty or whitespace")

    # 3. JWT format validation
    if not APIKeyValidator.validate_jwt_format(api_key):
        raise AuthenticationError(
            f"Invalid JWT token format. Expected format: header.payload.signature "
            f"with length {APIKeyValidator.MIN_LENGTH}-{APIKeyValidator.MAX_LENGTH} characters"
        )

    # 4. Decode and validate header
    header = APIKeyValidator.decode_jwt_header(api_key)
    if header is None:
        raise AuthenticationError("Unable to decode JWT token header")

    APIKeyValidator.validate_jwt_header(header)

    # 5. Decode and validate payload
    payload = APIKeyValidator.decode_jwt_payload(api_key)
    if payload is None:
        raise AuthenticationError("Unable to decode JWT token payload")

    # 6. Validate payload content
    APIKeyValidator.validate_jwt_payload(payload)

    # 7. Security validation
    APIKeyValidator.validate_security(api_key)

    return api_key


def get_token_info(api_key: str) -> Dict[str, Any]:
    """
    Extract information from JWT token for debugging/logging

    Args:
        api_key: Validated JWT token

    Returns:
        Dict with token information (safe for logging)
    """
    payload = APIKeyValidator.decode_jwt_payload(api_key)
    if not payload:
        return {"error": "Unable to decode token"}

    # Return safe information (no sensitive data)
    info = {
        "token_type": payload.get("type", "unknown"),
        "issued_at": datetime.fromtimestamp(payload["iat"]).isoformat() if "iat" in payload else None,
        "expires_at": datetime.fromtimestamp(payload["exp"]).isoformat() if "exp" in payload else None,
        "jti": payload.get("jti", "unknown")[:8] + "..." if "jti" in payload else None,  # Truncated for security
        "is_expired": payload.get("exp", 0) < datetime.now(timezone.utc).timestamp() if "exp" in payload else True
    }

    return info
