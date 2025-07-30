"""Utility functions for GMX V2 positions."""
from eth_abi.abi import encode
from eth_utils.crypto import keccak


def get_position_key(
    account: str, market: str, collateral_token: str, is_long: bool
) -> bytes:
    """Utility function to generate position keys."""
    key = keccak(
        encode(
            ["address", "address", "address", "bool"],
            [account, market, collateral_token, is_long],
        )
    )
    return key
