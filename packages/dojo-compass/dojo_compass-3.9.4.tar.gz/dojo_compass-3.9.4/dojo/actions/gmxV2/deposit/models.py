"""GmxDeposit actions for GMX."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from dataclasses_json import LetterCase, dataclass_json

from dojo.actions.gmxV2.base_gmx_action import InternalBaseGmxAction as BaseGmxAction
from dojo.actions.gmxV2.deposit.params import CreateDepositParams
from dojo.agents import BaseAgent
from dojo.observations.gmxV2 import GmxV2Observation


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxDepositProtobufMixin:
    """Mixin for creating deposits on GMX v2 to communicate with the dashboard."""

    deposit_id: int
    market_key: str
    initial_long_token_symbol: str  # TODO(aidar) Change to literals
    initial_short_token_symbol: str
    long_token_amount: Decimal
    short_token_amount: Decimal
    gm_token_amount: Decimal

    def get_proto_args(self) -> dict[str, str | int | Decimal]:
        """Function to return the proto args for the order."""
        return {
            "type": "CREATE_DEPOSIT",
            "market": self.market_key,
            "deposit_id": self.deposit_id,
            "initial_long_token_amount": self.long_token_amount,
            "initial_short_token_amount": self.short_token_amount,
            "initial_long_token_symbol": self.initial_long_token_symbol,
            "initial_short_token_symbol": self.initial_short_token_symbol,
            "min_market_tokens": self.gm_token_amount,
        }


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxDepositBase(BaseGmxAction):
    """Base LP order action on GMX v2."""

    create_deposit_params: CreateDepositParams
    original_key: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxHistoricDeposit(GmxDepositBase):
    """Action representing a historical LP order event on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxLPDeposit(GmxDepositBase, GmxDepositProtobufMixin):
    """Action representing a LP deposit on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class GmxDeposit(BaseGmxAction):
    """Data class for creating a LP deposit on GMX v2.

    :param agent: The agent creating the deposit.
    :param market_key: The market key for the deposit.
    :param initial_long_token_symbol: The initial long token symbol.
    :param initial_short_token_symbol: The initial short token symbol.
    :param long_token_usd: The amount of long token in USD.
    :param short_token_usd: The amount of short token in USD.
    :param observations: The observations object.
    :param gas: Optional gas units.
    :param gas_price: Optional gas price in wei.
    """

    market_key: str
    initial_long_token_symbol: str
    initial_short_token_symbol: str
    long_token_usd: Decimal
    short_token_usd: Decimal
    observations: GmxV2Observation

    __annotations__ = {
        "agent": BaseAgent,
        "market_key": str,
        "initial_long_token_symbol": str,
        "initial_short_token_symbol": str,
        "long_token_usd": Decimal,
        "short_token_usd": Decimal,
        "observations": GmxV2Observation,
    }
