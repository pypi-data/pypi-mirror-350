"""Main module for the igdbpy api wrapper"""

from .utils import generate_api_key
from .wrapper import IgdbWrapper

__all__ = [
    "IgdbWrapper",
    "generate_api_key",
]
