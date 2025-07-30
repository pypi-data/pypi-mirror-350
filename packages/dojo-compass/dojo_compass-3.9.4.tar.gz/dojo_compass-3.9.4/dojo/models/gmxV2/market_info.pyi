from dataclasses import dataclass
from typing import Any

@dataclass
class MarketProps:
    market_token: str
    index_token: str
    long_token: str
    short_token: str
    def __init__(self, market_token, index_token, long_token, short_token) -> None: ...

@dataclass
class CollateralType:
    long_token: int
    short_token: int
    def __init__(self, long_token, short_token) -> None: ...

@dataclass
class PositionType:
    long: CollateralType
    short: CollateralType
    def __init__(self, long, short) -> None: ...

@dataclass
class BaseFundingValues:
    funding_fee_amount_per_size: PositionType
    claimable_funding_amount_per_size: PositionType
    def __init__(self, funding_fee_amount_per_size, claimable_funding_amount_per_size) -> None: ...

@dataclass
class GetNextFundingAmountPerSizeResult:
    longs_pay_shorts: bool
    funding_factor_per_second: int
    next_saved_funding_factor_per_second: int
    funding_fee_amount_per_size: PositionType
    claimable_funding_amount_per_size: PositionType
    def __init__(self, longs_pay_shorts, funding_factor_per_second, next_saved_funding_factor_per_second, funding_fee_amount_per_size, claimable_funding_amount_per_size) -> None: ...

@dataclass
class VirtualInventory:
    virtual_pool_amount_for_long_token: int
    virtual_pool_amount_for_short_token: int
    virtual_pool_amount_for_positions: int
    def __init__(self, virtual_pool_amount_for_long_token, virtual_pool_amount_for_short_token, virtual_pool_amount_for_positions) -> None: ...

@dataclass
class MarketInfo:
    market: MarketProps
    borrowing_factor_per_second_for_longs: int
    borrowing_factor_per_second_for_shorts: int
    base_funding: BaseFundingValues
    next_funding: GetNextFundingAmountPerSizeResult
    virtual_inventory: VirtualInventory
    is_disabled: bool
    @classmethod
    def from_data(cls, data: Any) -> MarketInfo: ...
    def __init__(self, market, borrowing_factor_per_second_for_longs, borrowing_factor_per_second_for_shorts, base_funding, next_funding, virtual_inventory, is_disabled) -> None: ...
