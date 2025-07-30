"""This module defines the IGDB wrapper interface"""

import json
from typing import Dict, List

import requests

API_URL: str = "https://api.igdb.com/v4"


class IgdbWrapper:
    """The main wrapper for the IGDB API

    Attributes:
        client_id: Your client ID
        access_token: Your generated access token
        timeout: Number of seconds to wait before timing out a request
    """

    def __init__(self, client_id: str, access_token: str, timeout: int = 3) -> None:
        """Constructor for the IgdbWrapper

        Args:
            client_id: Your client ID
            access_token: Your generated access token
            timeout: Number of seconds to wait before timing out the connection
        """
        self.client_id = client_id
        self.access_token = access_token
        self.timeout = timeout

    def make_request(self, endpoint: str, field_query: str) -> List[Dict]:
        """Make a custom request on the IGDB API

        Args:
            endpoint: Specific endpoint to request
            field_query: The fields to gather and any filters placed on,
                this must be in the form 'fields {fields,}; {filters};
        Throws:
            Request error on bad status code
        """
        res = requests.post(
            f"{API_URL}/{endpoint}",
            data=field_query,
            headers=self._generic_header(),
            timeout=self.timeout,
        )
        res.raise_for_status()
        return list(json.loads(res.text))

    def request_game(self, field_query: str) -> List[Dict]:
        """Make a request on the game endpoint

        Args:
            field_query: The fields to gather and any filters placed on
        Throws:
            Request error on bad status code
        """
        return self.make_request("games", field_query)

    def _generic_header(self) -> Dict:
        return {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }
