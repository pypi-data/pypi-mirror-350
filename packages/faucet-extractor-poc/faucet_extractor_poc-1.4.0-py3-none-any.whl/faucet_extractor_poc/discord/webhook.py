from datetime import datetime
import os
import requests

from dotenv import load_dotenv

from ..utils.logger import setup_logger

load_dotenv()

logger = setup_logger("discord")


def send_workflow_run_alert(
    token_symbol: str,
    message: str,
    total_addresses: int,
    total_claimed: int,
    tries: int = 0,
) -> None:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "username": "Niagara Finance Bot",
        "embeds": [
            {
                "title": f"Summary for Scheduled Faucet Claim (${token_symbol}):",
                "footer": {"text": "Powered by Niagara Finance"},
                "timestamp": current_date,
                "description": message,
                "url": "https://niagarafinance.com",
                "color": 0x212121,
                "fields": [
                    {
                        "name": "Addresses",
                        "value": total_addresses,
                        "inline": True,
                    },
                    {
                        "name": "Claimed",
                        "value": total_claimed,
                        "inline": True,
                    },
                    {
                        "name": "Tries",
                        "value": tries,
                        "inline": True,
                    },
                ],
            }
        ],
    }

    if webhook_url:
        try:
            webhook_response = requests.post(webhook_url, json=data, timeout=10)
            if webhook_response.status_code == 204:
                logger.info("Notification sent to Discord webhook.")
            else:
                logger.error(
                    "Failed to send notification to Discord webhook. Status code: %d",
                    webhook_response.status_code,
                )
        except requests.exceptions.RequestException as e:
            logger.error("Failed to send notification to Discord webhook. Error: %s", e)
    else:
        logger.warning("No Discord webhook URL configured, skipping notification")
