from dataclasses import dataclass
from dojo.network.constants import ZERO_ADDRESS as ZERO_ADDRESS

@dataclass
class CreateDepositParamsAddresses:
    receiver: str
    market: str
    initial_long_token: str
    initial_short_token: str
    callback_contract: str = ...
    ui_fee_receiver: str = ...
    long_token_swap_path: list[str] = ...
    short_token_swap_path: list[str] = ...
    account: str | None = ...
    def __init__(self, receiver, market, initial_long_token, initial_short_token, callback_contract=..., ui_fee_receiver=..., long_token_swap_path=..., short_token_swap_path=..., account=...) -> None: ...

@dataclass
class CreateDepositParamsNumbers:
    initial_long_token_amount: int
    initial_short_token_amount: int
    min_market_tokens: int
    execution_fee: int
    callback_gas_limit: int
    def __init__(self, initial_long_token_amount, initial_short_token_amount, min_market_tokens, execution_fee, callback_gas_limit) -> None: ...

@dataclass
class CreateDepositParams:
    addresses: CreateDepositParamsAddresses
    numbers: CreateDepositParamsNumbers
    should_unwrap_native_token: bool
    def __init__(self, addresses, numbers, should_unwrap_native_token) -> None: ...
