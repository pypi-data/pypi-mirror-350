from typing import Optional, Dict, Any


class MistralClient:
    """A client for interacting with the Mistral API."""

    BASE_URL = 'https://api.mistral.ai/v1'

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize the Mistral client.

        Args:
            api_key (str): Your Mistral API key
            base_url (str, optional): Custom base URL for the API. Defaults to the official Mistral API URL.
        """

        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        self.default_payload = {
            'model': 'mistral-small-latest',
        }

    def _parse_response(self, response: Dict[str, Any]) -> str:
        """
        Parse the response from the Mistral API.
        """
        return ''.join([choice.get('message').get('content') for choice in response.get('choices')])

    def send_request(self, message: str, **kwargs) -> str:
        """
        Send a synchronous request to the Mistral API.

        Args:
            message (str): The message to send to the API
            **kwargs: Additional parameters to pass to the API

        Returns:
            str: The API response.
            If you receive several parts of answers, they will be merged in one
        """

        import requests

        url = f'{self.base_url}/chat/completions'

        payload = {
            'messages': [{'role': 'user', 'content': message}],
            **self.default_payload,
            **kwargs
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return self._parse_response(response=response.json())

    async def send_request_async(self, message: str, **kwargs) -> str:
        """
        Send an asynchronous request to the Mistral API.

        Args:
            message (str): The message to send to the API
            **kwargs: Additional parameters to pass to the API

        Returns:
            Dict[str, Any]: The API response
        """

        import aiohttp

        url = f'{self.base_url}/chat/completions'

        payload = {
            'messages': [{'role': 'user', 'content': message}],
            **self.default_payload,
            **kwargs
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                response.raise_for_status()
                return self._parse_response(response=await response.json())
