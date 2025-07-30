from dataclasses import dataclass
from dojo.network.constants import ZERO_ADDRESS as ZERO_ADDRESS
from enum import Enum

class OrderType(Enum):
    MARKET_SWAP = 0
    LIMIT_SWAP = 1
    MARKET_INCREASE = 2
    LIMIT_INCREASE = 3
    MARKET_DECREASE = 4
    LIMIT_DECREASE = 5
    STOP_LOSS_DECREASE = 6
    LIQUIDATION = 7

class DecreasePositionSwapType(Enum):
    NO_SWAP = 0
    SWAP_PNL_TOKEN_TO_COLLATERAL_TOKEN = 1
    SWAP_COLLATERAL_TOKEN_TO_PNL_TOKEN = 2

@dataclass
class CreateOrderParamsAddresses:
    receiver: str
    initial_collateral_token: str
    market: str
    cancellation_receiver: str = ...
    callback_contract: str = ...
    ui_fee_receiver: str = ...
    swap_path: list[str] = ...
    account: str | None = ...
    def __init__(self, receiver, initial_collateral_token, market, cancellation_receiver=..., callback_contract=..., ui_fee_receiver=..., swap_path=..., account=...) -> None: ...

@dataclass
class CreateOrderParamsNumbers:
    size_delta_usd: int
    initial_collateral_delta_amount: int
    trigger_price: int
    acceptable_price: int
    execution_fee: int
    callback_gas_limit: int
    min_output_amount: int
    def __init__(self, size_delta_usd, initial_collateral_delta_amount, trigger_price, acceptable_price, execution_fee, callback_gas_limit, min_output_amount) -> None: ...

@dataclass
class CreateOrderParams:
    addresses: CreateOrderParamsAddresses
    numbers: CreateOrderParamsNumbers
    order_type: OrderType
    decrease_position_swap_type: DecreasePositionSwapType
    is_long: bool
    should_unwrap_native_token: bool
    autoCancel: bool = ...
    referral_code: str = ...
    def __init__(self, addresses, numbers, order_type, decrease_position_swap_type, is_long, should_unwrap_native_token, autoCancel=..., referral_code=...) -> None: ...
