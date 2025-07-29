"""
Base faucet implementation that handles common functionality for all faucets.

This module defines a BaseFaucet class that implements common methods and attributes
for all blockchain faucet implementations, reducing code duplication.
"""

from abc import ABC
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

from ..utils.logger import setup_logger


load_dotenv()


@dataclass
class BaseFaucet(ABC):
    """Base class for all faucet implementations."""

    TOKEN_TICKER: str  # pylint: disable=C0103
    FAUCET_NAME: str  # pylint: disable=C0103
    FAUCET_URL: str  # pylint: disable=C0103

    def __post_init__(self):
        """Initialize the logger after dataclass initialization"""
        self.logger = setup_logger(self.FAUCET_NAME)

    def claim(self, address) -> tuple[bool, str, bool]:
        """
        Send a request to claim tokens from the faucet for the given address.

        Args:
            address (str): The blockchain address to receive tokens

        Returns:
            tuple:
                bool: True if the claim was successful, False otherwise
                str: Message describing the result
                bool: True if rate limited (should not retry), False otherwise
        """
        self.logger.info("Attempting to claim tokens for address: %s", address)

        payload = {
            "address": address,
            # "token": os.getenv("CAPTCHA_TOKEN"), # Required reCAPTCHA token
        }

        try:
            response = requests.post(self.FAUCET_URL, json=payload, timeout=10)

            success = response.status_code == 200
            rate_limited = False
            message = ""

            if success:
                message = (
                    f"Success: Address {address} processed on {self.FAUCET_NAME} faucet"
                )
                self.logger.info(message)
            else:
                # Check for rate limiting response
                is_json = response.headers.get("Content-Type") == "application/json"

                if is_json:
                    json_data = response.json()
                    # Check if this is a claim limit message
                    if (
                        isinstance(json_data, dict)
                        and json_data.get("message") == "Claim limit reached."
                    ):
                        rate_limited = True
                        remaining_time = json_data.get("remainingTime", 0) // 1000
                        hours = remaining_time // 3600
                        minutes = (remaining_time % 3600) // 60

                        message = (
                            f"Rate limited: Address {address} on {self.FAUCET_NAME} faucet - "
                            f"Claim limit reached. Wait time: ~{hours}h {minutes}m"
                        )
                        self.logger.warning(message)
                    else:
                        message = (
                            f"Failed: Address {address} on {self.FAUCET_NAME} faucet - "
                            f"Status: {response.status_code}, {json_data.get('message')}"
                        )
                        self.logger.error(message)
                else:
                    message = (
                        f"Failed: Address {address} on {self.FAUCET_NAME} -"
                        f"Status: {response.status_code}, {response.text}"
                    )
                    self.logger.error(message)

            return success, message, rate_limited
        except requests.exceptions.RequestException as e:
            message = f"Error: Failed to claim for address {address} on {self.FAUCET_NAME} - {str(e)}"
            self.logger.error(message)
            return False, message, False
