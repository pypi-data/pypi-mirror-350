"""Utility functions"""

import json
from dataclasses import dataclass

from requests import post


@dataclass
class Token:
    """Defines information pertaining to a generated access token

    Attributes:
        access_token: The token identifier to be used in further API usage
        expires_in: The number of seconds until this token expires
        token_type: The type of access this token provides
    """

    access_token: str
    expires_in: int
    token_type: str


def generate_api_key(client_id: str, client_secret: str, timeout: int = 5) -> Token:
    """Generate an access key for the API

    Args:
        client_id: Your client id
        client_secret: Your secret generated from your application management
        timeout: Number of seconds to wait before timing out
    Returns:
        Token instance generated in request
    Throws:
        Request exceptions based on status code
    """
    res = post(
        "https://id.twitch.tv/oauth2/token",
        params=[
            ("client_id", client_id),
            ("client_secret", client_secret),
            ("grant_type", "client_credentials"),
        ],
        timeout=timeout,
    )
    res.raise_for_status()

    data = json.loads(res.text)
    return Token(data["access_token"], data["expires_in"], data["token_type"])
