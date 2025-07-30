from dataclasses import dataclass
from decimal import Decimal
from dojo.actions.gmxV2.base_gmx_action import InternalBaseGmxAction as BaseGmxAction
from dojo.actions.gmxV2.orders.params import OrderType as OrderType
from dojo.agents import BaseAgent as BaseAgent
from dojo.observations.gmxV2 import GmxV2Observation as GmxV2Observation

@dataclass
class OrderDef:
    order_type: OrderType
    is_long: bool
    is_limit_order: bool
    def __init__(self, order_type, is_long, is_limit_order) -> None: ...

@dataclass
class GmxBaseTraderOrder(BaseGmxAction):
    agent: BaseAgent[GmxV2Observation]
    size_delta_usd: Decimal
    market_key: str
    token_in_symbol: str
    collateral_token_symbol: str
    observations: GmxV2Observation
    leverage: Decimal
    slippage: int
    def __init__(self, *generated_args, agent, size_delta_usd, market_key, token_in_symbol, collateral_token_symbol, observations, leverage, slippage, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxIncreaseLongMarketOrder(GmxBaseTraderOrder):
    def __init__(self, *generated_args, agent, size_delta_usd, market_key, token_in_symbol, collateral_token_symbol, observations, leverage, slippage, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxDecreaseLongMarketOrder(GmxBaseTraderOrder):
    def __init__(self, *generated_args, agent, size_delta_usd, market_key, token_in_symbol, collateral_token_symbol, observations, leverage, slippage, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxIncreaseShortMarketOrder(GmxBaseTraderOrder):
    def __init__(self, *generated_args, agent, size_delta_usd, market_key, token_in_symbol, collateral_token_symbol, observations, leverage, slippage, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxDecreaseShortMarketOrder(GmxBaseTraderOrder):
    def __init__(self, *generated_args, agent, size_delta_usd, market_key, token_in_symbol, collateral_token_symbol, observations, leverage, slippage, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxIncreaseLongLimitOrder(GmxBaseTraderOrder):
    trigger_price: Decimal
    def __init__(self, *generated_args, agent, size_delta_usd, market_key, token_in_symbol, collateral_token_symbol, observations, leverage, slippage, trigger_price, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxDecreaseLongLimitOrder(GmxBaseTraderOrder):
    trigger_price: Decimal
    def __init__(self, *generated_args, agent, size_delta_usd, market_key, token_in_symbol, collateral_token_symbol, observations, leverage, slippage, trigger_price, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxIncreaseShortLimitOrder(GmxBaseTraderOrder):
    trigger_price: Decimal
    def __init__(self, *generated_args, agent, size_delta_usd, market_key, token_in_symbol, collateral_token_symbol, observations, leverage, slippage, trigger_price, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxDecreaseShortLimitOrder(GmxBaseTraderOrder):
    trigger_price: Decimal
    def __init__(self, *generated_args, agent, size_delta_usd, market_key, token_in_symbol, collateral_token_symbol, observations, leverage, slippage, trigger_price, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxSwapOrder(BaseGmxAction):
    in_token: str
    out_token: str
    in_token_amount: Decimal
    slippage: int
    observations: GmxV2Observation
    def __init__(self, *generated_args, in_token, out_token, in_token_amount, slippage, observations, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...
