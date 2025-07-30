"""Actions for keepers to execute on GMX v2."""
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

from dojo.actions.gmxV2.base_gmx_action import InternalBaseGmxAction as BaseGmxAction


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SetPricesParams:
    """Params for setting prices on GMX v2."""

    tokens: list[str]
    providers: list[str]
    data: list[dict[str, int]]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxKeeperAction(BaseGmxAction):
    """Action representing a keeper action on GMX v2."""

    key: str
    block: int


@dataclass
class GmxExecuteOrderProfobufMixin:
    """Mixin for executing orders on GMX v2 to communicate with the dashboard."""

    order_id: int

    def get_proto_args(self) -> dict[str, str | int]:
        """Return the proto args for the execute order action."""
        return {"type": "EXECUTE_ORDER", "order_id": self.order_id}


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxExecuteDepositProfobufMixin:
    """Mixin for executing deposits on GMX v2 to communicate with the dashboard."""

    deposit_id: int

    def get_proto_args(self) -> dict[str, str | int]:
        """Return the proto args for the execute deposit action."""
        return {"type": "EXECUTE_DEPOSIT", "deposit_id": self.deposit_id}


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxExecuteWithdrawalProfobufMixin:
    """Mixin for executing withdrawals on GMX v2 to communicate with the dashboard."""

    withdrawal_id: int

    def get_proto_args(self) -> dict[str, str | int]:
        """Return the proto args for the execute withdrawal action."""
        return {"type": "EXECUTE_WITHDRAWAL", "withdrawal_id": self.withdrawal_id}


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxExecuteOrder(GmxKeeperAction, GmxExecuteOrderProfobufMixin):
    """Action representing an order execution event on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxExecuteDeposit(GmxKeeperAction, GmxExecuteDepositProfobufMixin):
    """Action representing an order execution event on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxExecuteWithdrawal(GmxKeeperAction, GmxExecuteWithdrawalProfobufMixin):
    """Action representing an order execution event on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxHistoricExecuteOrder(GmxKeeperAction):
    """Action representing a historical keeper action on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxHistoricExecuteDeposit(GmxKeeperAction):
    """Action representing a historical keeper action on GMX v2."""

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxHistoricExecuteWithdrawal(GmxKeeperAction):
    """Action representing a historical keeper action on GMX v2."""

    pass
