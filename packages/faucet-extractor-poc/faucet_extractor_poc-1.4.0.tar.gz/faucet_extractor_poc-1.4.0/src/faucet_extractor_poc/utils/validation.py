def is_valid_address(address):
    """Basic validation for Ethereum address format"""
    return (
        len(address) == 42
        and address.startswith("0x")
        and all(c in "0123456789abcdefABCDEF" for c in address[2:])
    )
