import argparse
import os
import sys
import time
from typing import List, Tuple

from dotenv import load_dotenv

from .discord.webhook import send_workflow_run_alert
from .utils.validation import is_valid_address
from .utils.logger import setup_logger
from .faucets.bera import BeraFaucet
from .faucets.monad import MonadFaucet

VALID_FAUCET_TYPES = {"BERA", "LUMIA", "MON", "IP"}

logger = setup_logger("extractor")


def process_address(address: str, faucet_type: str) -> tuple[bool, bool]:
    """
    Process a single ERC20 address for a specific faucet

    Returns:
        tuple: (success, rate_limited)
            - success: True if claim was successful
            - rate_limited: True if address is rate limited and should not be retried
    """
    try:
        if faucet_type == "BERA":
            bera_faucet = BeraFaucet()
            success, _, rate_limited = bera_faucet.claim(address)
            return success, rate_limited
        if faucet_type == "LUMIA":
            logger.info("Lumia faucet not implemented")
            return False, False
        if faucet_type == "MON":
            monad_faucet = MonadFaucet()
            success, _, rate_limited = monad_faucet.claim(address)
            return success, rate_limited
        if faucet_type == "IP":
            logger.info("IP faucet not implemented")
            return False, False
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(
            "Error processing address %s on faucet %s: %s", address, faucet_type, str(e)
        )
    return False, False


def _process_single_address(
    address: str, address_status: dict, faucet_type: str, max_retries: int
) -> bool:
    """
    Process a single address and update its status.
    Returns True if address needs to be retried, False otherwise.
    """
    if address_status[address]["success"] or address_status[address]["rate_limited"]:
        return False

    if address_status[address]["failed"] >= max_retries:
        logger.warning(
            "Address %s reached max retries (%d), skipping",
            address,
            max_retries,
        )
        return False

    success, rate_limited = process_address(address, faucet_type)

    if success:
        address_status[address]["success"] = True
    elif rate_limited:
        address_status[address]["rate_limited"] = True
        logger.info("Address %s is rate limited, skipping future retries", address)
    else:
        address_status[address]["failed"] += 1
        return True  # Needs retry

    return False  # No need to retry


def _is_processing_complete(
    address_status: dict, max_retries: int, attempt: int
) -> bool:
    """
    Check if processing is complete based on address statuses and attempt count.
    """
    all_done = all(
        status["success"] or status["rate_limited"] or status["failed"] >= max_retries
        for status in address_status.values()
    )

    return all_done or attempt >= max_retries


def _log_final_status(
    address_status: dict, addresses: List[str], faucet_type: str, attempt: int
) -> None:
    """
    Log final status and send alerts.
    """
    successful_count = sum(1 for status in address_status.values() if status["success"])
    rate_limited_count = sum(
        1 for status in address_status.values() if status["rate_limited"]
    )

    # Print final status
    logger.info("Final Status:")
    for address, status in address_status.items():
        if status["success"]:
            logger.info("Address %s: Succeeded", address)
        elif status["rate_limited"]:
            logger.info("Address %s: Rate limited (skipped)", address)
        else:
            logger.info(
                "Address %s: Failed after %d attempts", address, status["failed"]
            )

    alert_message = "Workflow run completed."
    details = []
    if successful_count > 0:
        details.append(f"{successful_count} addresses succeeded")
    if rate_limited_count > 0:
        details.append(f"{rate_limited_count} addresses rate limited")
    if len(addresses) - successful_count - rate_limited_count > 0:
        details.append(
            f"{len(addresses) - successful_count - rate_limited_count} addresses failed"
        )

    if details:
        alert_message += " " + ", ".join(details) + "."

    send_workflow_run_alert(
        faucet_type, alert_message, len(addresses), successful_count, attempt
    )


def process_addresses_with_retries(
    addresses: List[str], faucet_type: str, max_retries: int = 10
) -> Tuple[dict, int]:
    """
    Process addresses with retries for failed attempts.
    Returns the address status and the number of attempts made.
    """
    # Track addresses and their statuses
    address_status = {
        addr: {"failed": 0, "success": False, "rate_limited": False}
        for addr in addresses
    }

    attempt = 1
    while True:
        failed_addresses = []
        logger.info("Attempt %d of %d", attempt, max_retries)

        # Process only addresses that haven't succeeded or been rate limited
        for address in addresses:
            needs_retry = _process_single_address(
                address, address_status, faucet_type, max_retries
            )
            if needs_retry:
                failed_addresses.append(address)
            time.sleep(5)

        # Check if all addresses succeeded, are rate limited, or reached max retries
        if _is_processing_complete(address_status, max_retries, attempt):
            break

        if failed_addresses:
            logger.info("Retrying failed addresses: %s", failed_addresses)
            time.sleep(30)  # Wait 30 seconds before retrying

        attempt += 1

    _log_final_status(address_status, addresses, faucet_type, attempt)
    return address_status, attempt


def main():
    parser = argparse.ArgumentParser(
        description="Process ERC20 token addresses with specific faucet type"
    )
    parser.add_argument(
        "-f",
        "--faucet",
        required=True,
        type=lambda s: s.upper(),
        choices=VALID_FAUCET_TYPES,
        help=f'Faucet type to use ({", ".join(VALID_FAUCET_TYPES)})',
    )
    parser.add_argument(
        "addresses",
        nargs="*",
        help="ERC20 token addresses (space-separated) or use ERC20_ADDRESSES env var",
    )

    args = parser.parse_args()

    # Get faucet type
    faucet_type = args.faucet
    logger.info("Starting extraction for faucet type: %s", faucet_type)

    # Initialize addresses list
    addresses = []

    # First check if addresses were provided via CLI
    if args.addresses:
        addresses = args.addresses
    else:
        # If no CLI args, fall back to environment variable
        addresses_str = os.environ.get("ERC20_ADDRESSES", "")
        if addresses_str:
            addresses = [addr.strip() for addr in addresses_str.split(",")]

    # If still no addresses, exit with error
    if not addresses:
        logger.error(
            "Error: No addresses provided. "
            "Either provide addresses as arguments or set ERC20_ADDRESSES env variable"
        )
        sys.exit(1)

    # Validate addresses
    valid_addresses = []
    for address in addresses:
        if not address:
            continue
        if not is_valid_address(address):
            logger.warning("Invalid address format: %s, skipping", address)
            continue
        valid_addresses.append(address)

    if not valid_addresses:
        logger.error("No valid addresses to process")
        sys.exit(1)

    logger.info("Processing %d valid addresses", len(valid_addresses))

    # Process addresses with retries
    process_addresses_with_retries(
        valid_addresses, faucet_type, max_retries=max(1, len(valid_addresses) // 2)
    )


if __name__ == "__main__":
    load_dotenv()

    try:
        main()
    except (ValueError, TypeError, RuntimeError, KeyboardInterrupt) as e:
        print(str(e))
        sys.exit(1)
