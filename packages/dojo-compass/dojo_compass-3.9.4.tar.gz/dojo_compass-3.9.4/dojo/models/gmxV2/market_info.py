"""Market info model for GMX V2."""

from dataclasses import dataclass
from typing import Any

from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MarketProps:
    """Market properties representation in GMX."""

    market_token: str
    index_token: str
    long_token: str
    short_token: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CollateralType:
    """Collateral type representation in GMX."""

    long_token: int
    short_token: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PositionType:
    """Position type representation in GMX."""

    long: CollateralType
    short: CollateralType


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class BaseFundingValues:
    """Base funding values representation in GMX."""

    funding_fee_amount_per_size: PositionType
    claimable_funding_amount_per_size: PositionType


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GetNextFundingAmountPerSizeResult:
    """Funding amount representation in GMX."""

    longs_pay_shorts: bool
    funding_factor_per_second: int
    next_saved_funding_factor_per_second: int
    funding_fee_amount_per_size: PositionType
    claimable_funding_amount_per_size: PositionType


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class VirtualInventory:
    """Virtual inventory representation in GMX."""

    virtual_pool_amount_for_long_token: int
    virtual_pool_amount_for_short_token: int
    virtual_pool_amount_for_positions: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MarketInfo:
    """Market info representation in GMX."""

    market: MarketProps
    borrowing_factor_per_second_for_longs: int
    borrowing_factor_per_second_for_shorts: int
    base_funding: BaseFundingValues
    next_funding: GetNextFundingAmountPerSizeResult
    virtual_inventory: VirtualInventory
    is_disabled: bool

    @classmethod
    def from_data(cls, data: Any) -> "MarketInfo":
        """Create MarketInfo from data."""
        market_props = MarketProps(*data[0])
        base_funding = BaseFundingValues(
            PositionType(
                CollateralType(*data[3][0][0]), CollateralType(*data[3][0][1])
            ),
            PositionType(
                CollateralType(*data[3][1][0]), CollateralType(*data[3][1][1])
            ),
        )
        next_funding = GetNextFundingAmountPerSizeResult(
            data[4][0],
            data[4][1],
            data[4][2],
            PositionType(
                CollateralType(*data[4][3][0]), CollateralType(*data[4][3][1])
            ),
            PositionType(
                CollateralType(*data[4][4][0]), CollateralType(*data[4][4][1])
            ),
        )
        virtual_inventory = VirtualInventory(*data[5])
        return cls(
            market=market_props,
            borrowing_factor_per_second_for_longs=data[1],
            borrowing_factor_per_second_for_shorts=data[2],
            base_funding=base_funding,
            next_funding=next_funding,
            virtual_inventory=virtual_inventory,
            is_disabled=data[6],
        )
