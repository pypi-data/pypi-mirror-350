from dataclasses import dataclass
from decimal import Decimal
from dojo.actions.gmxV2.base_gmx_action import InternalBaseGmxAction as BaseGmxAction
from dojo.actions.gmxV2.withdrawal.params import CreateWithdrawalParams as CreateWithdrawalParams

@dataclass
class GmxWithdrawalProtobufMixin:
    withdrawal_id: int
    market_key: str
    gm_token_amount: Decimal
    def get_proto_args(self) -> dict[str, str | int | Decimal]: ...
    def __init__(self, withdrawal_id, market_key, gm_token_amount) -> None: ...

@dataclass
class GmxWithdrawalBase(BaseGmxAction):
    create_withdrawal_params: CreateWithdrawalParams
    original_key: str | None = ...
    def __init__(self, *generated_args, create_withdrawal_params, original_key=..., agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxHistoricWithdrawal(GmxWithdrawalBase):
    def __init__(self, *generated_args, create_withdrawal_params, original_key=..., agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxLPWithdrawal(GmxWithdrawalBase, GmxWithdrawalProtobufMixin):
    def __init__(self, *generated_args, withdrawal_id, market_key, gm_token_amount, create_withdrawal_params, original_key=..., agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxWithdrawal(BaseGmxAction):
    market_key: str
    gm_token_amount: Decimal
    __annotations__ = ...
    def __init__(self, *generated_args, market_key, gm_token_amount, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...
