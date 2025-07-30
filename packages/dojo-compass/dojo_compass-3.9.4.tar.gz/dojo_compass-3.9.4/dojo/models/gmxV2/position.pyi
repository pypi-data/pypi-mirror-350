from _typeshed import Incomplete
from dataclasses import dataclass
from decimal import Decimal
from hexbytes import HexBytes

ORACLE_DECIMALS: int
ORACLE_SCALING_FACTOR: Incomplete

@dataclass
class Addresses:
    account: str
    market: str
    collateral_token: str
    def __init__(self, account, market, collateral_token) -> None: ...

@dataclass
class Numbers:
    size_in_usd: int
    size_in_tokens: int
    collateral_amount: int
    borrowing_factor: int
    funding_fee_amount_per_size: int
    long_token_claimable_funding_amount_per_size: int
    short_token_claimable_funding_amount_per_size: int
    increased_at_block: int
    decreased_at_block: int
    increased_at_time: int
    decreased_at_time: int
    def __init__(self, size_in_usd, size_in_tokens, collateral_amount, borrowing_factor, funding_fee_amount_per_size, long_token_claimable_funding_amount_per_size, short_token_claimable_funding_amount_per_size, increased_at_block, decreased_at_block, increased_at_time, decreased_at_time) -> None: ...

@dataclass
class Flags:
    is_long: bool
    def __init__(self, is_long) -> None: ...

@dataclass
class Position:
    addresses: Addresses
    numbers: Numbers
    flags: Flags
    @classmethod
    def from_data(cls, data: list[tuple[tuple[str], tuple[int], tuple[bool]]]) -> list['Position']: ...
    @property
    def key(self) -> HexBytes: ...
    def __init__(self, addresses, numbers, flags) -> None: ...

@dataclass
class PositionPnl:
    position_pnl_usd: Decimal
    uncapped_position_pnl_usd: Decimal
    size_delta_in_tokens: Decimal
    def __post_init__(self) -> None: ...
    def __init__(self, position_pnl_usd, uncapped_position_pnl_usd, size_delta_in_tokens) -> None: ...
