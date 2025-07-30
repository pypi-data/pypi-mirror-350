from dataclasses import dataclass
from decimal import Decimal
from dojo.actions.gmxV2.base_gmx_action import InternalBaseGmxAction as BaseGmxAction
from dojo.actions.gmxV2.deposit.params import CreateDepositParams as CreateDepositParams
from dojo.agents import BaseAgent as BaseAgent
from dojo.observations.gmxV2 import GmxV2Observation as GmxV2Observation

@dataclass
class GmxDepositProtobufMixin:
    deposit_id: int
    market_key: str
    initial_long_token_symbol: str
    initial_short_token_symbol: str
    long_token_amount: Decimal
    short_token_amount: Decimal
    gm_token_amount: Decimal
    def get_proto_args(self) -> dict[str, str | int | Decimal]: ...
    def __init__(self, deposit_id, market_key, initial_long_token_symbol, initial_short_token_symbol, long_token_amount, short_token_amount, gm_token_amount) -> None: ...

@dataclass
class GmxDepositBase(BaseGmxAction):
    create_deposit_params: CreateDepositParams
    original_key: str | None = ...
    def __init__(self, *generated_args, create_deposit_params, original_key=..., agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxHistoricDeposit(GmxDepositBase):
    def __init__(self, *generated_args, create_deposit_params, original_key=..., agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxLPDeposit(GmxDepositBase, GmxDepositProtobufMixin):
    def __init__(self, *generated_args, deposit_id, market_key, initial_long_token_symbol, initial_short_token_symbol, long_token_amount, short_token_amount, gm_token_amount, create_deposit_params, original_key=..., agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass(kw_only=True)
class GmxDeposit(BaseGmxAction):
    market_key: str
    initial_long_token_symbol: str
    initial_short_token_symbol: str
    long_token_usd: Decimal
    short_token_usd: Decimal
    observations: GmxV2Observation
    __annotations__ = ...
    def __init__(self, *generated_args, agent, gas=..., gas_price=..., market_key, initial_long_token_symbol, initial_short_token_symbol, long_token_usd, short_token_usd, observations, **generated_kwargs) -> None: ...
