"""Parameters required to communicate with GMX v2 deposit creation."""
from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import LetterCase, dataclass_json

from dojo.network.constants import ZERO_ADDRESS


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateDepositParamsAddresses:
    """Addresses to be used for creating a deposit on GMX v2."""

    receiver: str
    market: str
    initial_long_token: str
    initial_short_token: str
    callback_contract: str = ZERO_ADDRESS
    ui_fee_receiver: str = ZERO_ADDRESS
    long_token_swap_path: list[str] = field(default_factory=list)
    short_token_swap_path: list[str] = field(default_factory=list)
    account: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateDepositParamsNumbers:
    """Numbers to be used for creating a deposit on GMX v2."""

    initial_long_token_amount: int
    initial_short_token_amount: int
    min_market_tokens: int
    execution_fee: int
    callback_gas_limit: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateDepositParams:
    """Dataclass representing a deposit on GMX v2."""

    addresses: CreateDepositParamsAddresses
    numbers: CreateDepositParamsNumbers
    should_unwrap_native_token: bool
