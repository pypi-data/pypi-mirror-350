"""Parameters required to communicate with GMX v2 deposit withdrawal."""
from dataclasses import dataclass
from typing import Optional

from dataclasses_json import LetterCase, dataclass_json

from dojo.network.constants import ZERO_ADDRESS


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateWithdrawalParams:
    """Parameters required to create a withdrawal on GMX v2."""

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
    ui_fee_receiver: Optional[str] = ZERO_ADDRESS
