"""
ContactedAI Python SDK
Official Python client for the ContactedAI API
"""

import requests
from typing import Dict, Any, Optional
from .validation import validate_send_options


class ContactedAI:
    """ContactedAI API client"""

    def __init__(self, api_key: str, base_url: str = "https://api.contacted.io", timeout: int = 30):
        """
        Initialize ContactedAI client

        Args:
            api_key (str): Your ContactedAI API key
            base_url (str, optional): Custom API base URL
            timeout (int, optional): Request timeout in seconds

        Raises:
            ValueError: If API key is not provided
        """
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

        # Setup session with default headers
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer ${self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'contacted-python/1.0.0'
        })

    def send(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a message through the ContactedAI API

        Args:
            options (dict): Send options containing:
                - from (str): Sender email address
                - to (str): Receiver email address
                - prompt (str): AI prompt (10-250 characters)
                - data (dict, optional): Additional data for personalization

        Returns:
            dict: API response

        Raises:
            ValueError: If validation fails
            requests.RequestException: If API request fails
        """
        # Validate input before making API call
        validate_send_options(options)

        payload = {
            'from': options['from'],
            'to': options['to'],
            'prompt': options['prompt'],
            'data': options.get('data', {})
        }

        try:
            response = self.session.post(
                f"{self.base_url}/send",
                json=payload,
                timeout=self.timeout
            )

            # Handle different response status codes
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json() if response.content else {}
                error_message = error_data.get('message', 'Bad request')
                raise ValueError(f"ContactedAI API Error: {error_message}")
            elif response.status_code == 401:
                raise ValueError("ContactedAI API Error: Invalid API key")
            elif response.status_code == 429:
                raise ValueError("ContactedAI API Error: Rate limit exceeded")
            elif response.status_code >= 500:
                raise ValueError("ContactedAI API Error: Server error")
            else:
                response.raise_for_status()

        except requests.exceptions.Timeout:
            raise ValueError("Network error: Request timeout")
        except requests.exceptions.ConnectionError:
            raise ValueError("Network error: Unable to reach ContactedAI API")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request error: {str(e)}")

    def status(self) -> Dict[str, Any]:
        """
        Check API status and health

        Returns:
            dict: Status information

        Raises:
            requests.RequestException: If API request fails
        """
        try:
            response = self.session.get(
                f"{self.base_url}/status",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get status: {str(e)}")