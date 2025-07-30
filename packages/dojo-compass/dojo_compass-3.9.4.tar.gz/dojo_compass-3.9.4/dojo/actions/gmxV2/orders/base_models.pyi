from dataclasses import dataclass
from decimal import Decimal
from dojo.actions.gmxV2.base_gmx_action import InternalBaseGmxAction as BaseGmxAction
from dojo.actions.gmxV2.orders.params import CreateOrderParams as CreateOrderParams
from dojo.money.format import to_human_format as to_human_format
from dojo.network.constants import GMX_ORACLE_PRECISION as GMX_ORACLE_PRECISION

@dataclass
class GmxOrderProtobufMixin:
    market_key: str
    leverage: Decimal
    token_in_symbol: str
    collateral_symbol: str
    order_id: int
    def get_proto_args(self) -> dict[str, str | Decimal | int]: ...
    def __init__(self, market_key, leverage, token_in_symbol, collateral_symbol, order_id) -> None: ...

@dataclass
class GmxOrderBase(BaseGmxAction):
    create_order_params: CreateOrderParams
    original_key: str | None = ...
    def __init__(self, *generated_args, create_order_params, original_key=..., agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxHistoricOrder(GmxOrderBase):
    out_token: str | None = ...
    def __init__(self, *generated_args, create_order_params, original_key=..., out_token=..., agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxOrder(GmxOrderBase, GmxOrderProtobufMixin):
    out_token: str | None = ...
    def get_size_delta_usd(self) -> Decimal: ...
    def __init__(self, *generated_args, market_key, leverage, token_in_symbol, collateral_symbol, order_id, create_order_params, original_key=..., out_token=..., agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxCancelOrder(BaseGmxAction):
    account: str
    key: str
    reasonBytes: str
    reason: str
    def __init__(self, *generated_args, account, key, reasonBytes, reason, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxUpdateOrder(BaseGmxAction):
    key: str
    size_delta_usd: int
    acceptable_price: int
    trigger_price: int
    min_output_amount: int
    account: str
    auto_cancel: bool = ...
    def __init__(self, *generated_args, key, size_delta_usd, acceptable_price, trigger_price, min_output_amount, account, auto_cancel=..., agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxHistoricOrderCancel(GmxCancelOrder):
    def __init__(self, *generated_args, account, key, reasonBytes, reason, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxHistoricOrderUpdate(GmxUpdateOrder):
    def __init__(self, *generated_args, key, size_delta_usd, acceptable_price, trigger_price, min_output_amount, account, auto_cancel=..., agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...
