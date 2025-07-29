"""
Base API client for Voyado Engage.
"""

import requests
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin
import json

from .exceptions import (
    VoyadoAPIError,
    VoyadoAuthenticationError,
    VoyadoRateLimitError,
    VoyadoValidationError,
    VoyadoNotFoundError,
)


class BaseAPIClient:
    """Base class for API operations."""
    
    def __init__(self, api_key: str, base_url: str, user_agent: str = "VoyadoPython/0.1.0"):
        """
        Initialize the base API client.
        
        Args:
            api_key: Your Voyado API key
            base_url: Base URL for your Voyado instance (e.g., https://yourinstance.voyado.com)
            user_agent: User agent string for API requests
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.user_agent = user_agent
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Set up the requests session with default headers."""
        self.session.headers.update({
            'apikey': self.api_key,
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
    
    def _build_url(self, endpoint: str) -> str:
        """Build the full URL for an API endpoint."""
        # Ensure endpoint starts with /api/v3 if not already
        if not endpoint.startswith('/api/'):
            endpoint = f'/api/v3{endpoint}'
        return urljoin(self.base_url, endpoint)

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions."""
        try:
            response_data = response.json() if response.content else {}
        except json.JSONDecodeError:
            response_data = {"error": response.text}
        
        if response.status_code == 200:
            return response_data
        elif response.status_code == 201:
            return response_data
        elif response.status_code == 202:
            return response_data
        elif response.status_code == 204:
            return {}
        elif response.status_code == 400:
            raise VoyadoValidationError(
                response_data.get('message', 'Validation error'),
                status_code=400,
                response_data=response_data
            )
        elif response.status_code == 401:
            raise VoyadoAuthenticationError(
                'Authentication failed. Check your API key.',
                status_code=401,
                response_data=response_data
            )
        elif response.status_code == 404:
            raise VoyadoNotFoundError(
                response_data.get('message', 'Resource not found'),
                status_code=404,
                response_data=response_data
            )
        elif response.status_code == 429:
            raise VoyadoRateLimitError(
                'Rate limit exceeded. Please try again later.',
                status_code=429,
                response_data=response_data
            )
        else:
            raise VoyadoAPIError(
                f'API error: {response.status_code}',
                status_code=response.status_code,
                response_data=response_data
            )

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make an API request."""
        url = self._build_url(endpoint)
        
        # Merge headers
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        # Make the request
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=request_headers,
        )
        
        return self._handle_response(response)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self._request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request."""
        return self._request('POST', endpoint, data=data, params=params)
    
    def patch(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PATCH request."""
        return self._request('PATCH', endpoint, data=data, params=params)
    
    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._request('DELETE', endpoint, params=params)
