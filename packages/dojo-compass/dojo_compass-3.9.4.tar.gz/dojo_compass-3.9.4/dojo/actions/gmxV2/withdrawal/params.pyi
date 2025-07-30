from dataclasses import dataclass
from dojo.network.constants import ZERO_ADDRESS as ZERO_ADDRESS

@dataclass
class CreateWithdrawalParams:
    receiver: str
    callback_contract: str
    market: str
    long_token_swap_path: list[str]
    short_token_swap_path: list[str]
    min_long_token_amount: int
    min_short_token_amount: int
    market_token_amount: int
    execution_fee: int
    callback_gas_limit: int
    should_unwrap_native_token: bool
    ui_fee_receiver: str | None = ...
    def __init__(self, receiver, callback_contract, market, long_token_swap_path, short_token_swap_path, min_long_token_amount, min_short_token_amount, market_token_amount, execution_fee, callback_gas_limit, should_unwrap_native_token, ui_fee_receiver=...) -> None: ...
