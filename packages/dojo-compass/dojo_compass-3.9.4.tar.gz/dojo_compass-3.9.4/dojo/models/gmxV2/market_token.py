"""Market token model for GMX V2."""
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MarketPoolValueInfo:
    """Information about the market pool value."""

    pool_value: int
    long_pnl: int
    short_pnl: int
    net_pnl: int
    long_token_amount: int
    short_token_amount: int
    long_token_usd: int
    short_token_usd: int
    total_borrowing_fees: int
    borrowing_fee_pool_factor: int
    impact_pool_amount: int
