"""
This script defines a class to interact with the Bera faucet for claiming tokens.
It inherits from BaseFaucet to leverage common faucet functionality.

Classes:
    BeraFaucet: A class to handle the interaction with the Bera faucet.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from .base import BaseFaucet

load_dotenv()


@dataclass
class BeraFaucet(BaseFaucet):
    """Implementation for the Bera blockchain faucet."""

    TOKEN_TICKER: str = "BERA"
    FAUCET_NAME: str = "Bera"
    FAUCET_URL: str = os.getenv("BERA_FAUCET_URL")
