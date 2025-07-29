"""
This script defines a class to interact with the Monad faucet for claiming tokens.
It inherits from BaseFaucet to leverage common faucet functionality.

Classes:
    MonadFaucet: A class to handle the interaction with the Monad faucet.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from .base import BaseFaucet

load_dotenv()


@dataclass
class MonadFaucet(BaseFaucet):
    """Implementation for the Monad blockchain faucet."""

    TOKEN_TICKER: str = "MON"
    FAUCET_NAME: str = "Monad"
    FAUCET_URL: str = os.getenv("MONAD_FAUCET_URL")
