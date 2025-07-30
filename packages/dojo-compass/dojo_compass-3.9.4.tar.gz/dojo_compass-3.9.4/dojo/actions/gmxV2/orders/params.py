"""Parameters required to communicate with GMX v2 order creation."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from dataclasses_json import LetterCase, dataclass_json

from dojo.network.constants import ZERO_ADDRESS


class OrderType(Enum):
    """Possible order types on GMX v2."""

    MARKET_SWAP = 0
    LIMIT_SWAP = 1
    MARKET_INCREASE = 2
    LIMIT_INCREASE = 3
    MARKET_DECREASE = 4
    LIMIT_DECREASE = 5
    STOP_LOSS_DECREASE = 6
    LIQUIDATION = 7


class DecreasePositionSwapType(Enum):
    """Possible decrease position swap types."""

    NO_SWAP = 0
    SWAP_PNL_TOKEN_TO_COLLATERAL_TOKEN = 1
    SWAP_COLLATERAL_TOKEN_TO_PNL_TOKEN = 2


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateOrderParamsAddresses:
    """Addresses to be used for creating an order on GMX v2."""

    receiver: str
    initial_collateral_token: str
    market: str
    cancellation_receiver: str = ZERO_ADDRESS
    callback_contract: str = ZERO_ADDRESS
    ui_fee_receiver: str = ZERO_ADDRESS
    swap_path: list[str] = field(default_factory=list)
    account: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateOrderParamsNumbers:
    """This data class is used to define order when one is created."""

    size_delta_usd: int  # when closing position, this must be negative
    initial_collateral_delta_amount: int
    trigger_price: int
    acceptable_price: int
    execution_fee: int
    callback_gas_limit: int
    min_output_amount: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateOrderParams:
    """Parameters for creating an order."""

    addresses: CreateOrderParamsAddresses
    numbers: CreateOrderParamsNumbers
    order_type: OrderType
    decrease_position_swap_type: DecreasePositionSwapType
    is_long: bool
    should_unwrap_native_token: bool
    autoCancel: bool = False
    referral_code: str = (
        "0x0000000000000000000000000000000000000000000000000000000000000000"
    )
