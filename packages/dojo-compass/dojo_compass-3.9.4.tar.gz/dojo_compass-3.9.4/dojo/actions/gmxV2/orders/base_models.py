"""GmxOrder actions for GMX v2."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from dataclasses_json import LetterCase, dataclass_json

from dojo.actions.gmxV2.base_gmx_action import InternalBaseGmxAction as BaseGmxAction
from dojo.actions.gmxV2.orders.params import CreateOrderParams
from dojo.money.format import to_human_format
from dojo.network.constants import GMX_ORACLE_PRECISION


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxOrderProtobufMixin:
    """Mixin for creating orders on GMX v2 to communicate with the dashboard."""

    market_key: str
    leverage: Decimal
    token_in_symbol: str
    collateral_symbol: str
    order_id: int

    def get_proto_args(self) -> dict[str, str | Decimal | int]:
        """Function to return the proto args for the order."""
        return {
            "type": self.create_order_params.order_type.name,  # type: ignore
            "market": self.market_key,
            "usd_value": self.get_size_delta_usd(),  # type: ignore
            "leverage": self.leverage,
            "token_in_symbol": self.token_in_symbol,
            "collateral_symbol": self.collateral_symbol,
            "is_long": self.create_order_params.is_long,  # type: ignore
            "order_id": self.order_id,
        }


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxOrderBase(BaseGmxAction):
    """Base action representing an order."""

    create_order_params: CreateOrderParams
    original_key: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxHistoricOrder(GmxOrderBase):
    """Action representing a historical order event on GMX v2."""

    out_token: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxOrder(GmxOrderBase, GmxOrderProtobufMixin):
    """Base trader order action on GMX v2."""

    out_token: Optional[str] = None

    def get_size_delta_usd(self) -> Decimal:
        """Function to return the size delta in USD."""
        return to_human_format(
            self.create_order_params.numbers.size_delta_usd, GMX_ORACLE_PRECISION
        )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxCancelOrder(BaseGmxAction):
    """Base action representing an order cancel."""

    account: str
    key: str
    reasonBytes: str
    reason: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxUpdateOrder(BaseGmxAction):
    """Action representing an order update on GMX v2."""

    key: str
    size_delta_usd: int
    acceptable_price: int
    trigger_price: int
    min_output_amount: int
    account: str
    auto_cancel: bool = False


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxHistoricOrderCancel(GmxCancelOrder):
    """Action representing a historical order cancelling event on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxHistoricOrderUpdate(GmxUpdateOrder):
    """Action representing a historical order update on GMX v2."""

    pass
