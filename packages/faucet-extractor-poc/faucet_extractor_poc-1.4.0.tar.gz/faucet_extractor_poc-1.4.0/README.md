# Faucet Extractor PoC

This project is a Proof of Concept (PoC) for a faucet extractor. It sends a request to a given URL of a faucet and tries to claim a testnet token.

## Features

- Sends a request to a specified faucet URL
- Attempts to claim testnet tokens

## Requirements

- Python 3.10
- `requests` library
- `python-dotenv` library

## Environment Variables

The following environment variables need to be set before using the project:

- `DISCORD_WEBHOOK_URL` (optional) - Discord webhook URL for notifications
- `ERC20_ADDRESSES` - Comma-separated list of ERC20 addresses
- `BERA_FAUCET_URL` - Bera faucet URL
- `MONAD_FAUCET_URL` - Monad faucet URL

## Installation

### Method 1: Install from PyPI (Recommended)

Install the package directly from PyPI:

```bash
pip install faucet-extractor-poc
```

### Method 2: Install from Source

1. Clone the repository:

    ```bash
    git clone https://github.com/niagarafinance/faucet-extractor-poc.git
    ```

2. Navigate to the project directory:

    ```bash
    cd faucet-extractor-poc
    ```

3. Install the package in development mode:

    ```bash
    pip install -e .
    ```

## Usage

Before running the project, make sure to set the required environment variables.

```bash
export BERA_FAUCET_URL="https://bera-faucet-url.com"
export MONAD_FAUCET_URL="https://monad-faucet-url.com"
```

To run the project, use the appropriate command:

### Using the installed package

```bash
faucet-extractor --faucet MON 0x1234567890123456789012345678901234567890
```

### Multiple addresses with faucet type

```bash
faucet-extractor --faucet BERA 0xAddress1 0xAddress2 0xAddress3
```

### Using environment variable with faucet

```bash
export ERC20_ADDRESSES="0xAddress1,0xAddress2"
faucet-extractor --faucet BERA
```

### Running directly from the source

If you installed from source, you can also run the module directly:

```bash
python -m src.faucet_extractor_poc.extract --faucet MON 0x1234567890123456789012345678901234567890
```

### Show help

```bash
faucet-extractor --help
```

