"""GmxWithdrawal action models for GMX v2."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from dataclasses_json import LetterCase, dataclass_json

from dojo.actions.gmxV2.base_gmx_action import InternalBaseGmxAction as BaseGmxAction
from dojo.actions.gmxV2.withdrawal.params import CreateWithdrawalParams


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxWithdrawalProtobufMixin:
    """Mixin for creating withdrawals on GMX v2 to communicate with the dashboard."""

    withdrawal_id: int
    market_key: str
    gm_token_amount: Decimal

    def get_proto_args(self) -> dict[str, str | int | Decimal]:
        """Function to return the proto args for the order."""
        return {
            "type": "CREATE_WITHDRAWAL",
            "market": self.market_key,
            "withdrawal_id": self.withdrawal_id,
            "min_market_tokens": self.gm_token_amount,
        }


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxWithdrawalBase(BaseGmxAction):
    """Action representing a withdrawal on GMX v2."""

    create_withdrawal_params: CreateWithdrawalParams
    original_key: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxHistoricWithdrawal(GmxWithdrawalBase):
    """Action representing a historical withdrawal event on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxLPWithdrawal(GmxWithdrawalBase, GmxWithdrawalProtobufMixin):
    """Action representing a LP withdrawal on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxWithdrawal(BaseGmxAction):
    """Action representing a withdrawal on GMX v2.

    :param agent: The agent executing the action.
    :param market_key: The market key.
    :param gm_token_amount: The GM token amount.
    :param gas: Optional gas units.
    :param gas_price: Optional gas price in wei.
    """

    market_key: str
    gm_token_amount: Decimal

    __annotations__ = {
        "market_key": str,
        "gm_token_amount": Decimal,
    }
