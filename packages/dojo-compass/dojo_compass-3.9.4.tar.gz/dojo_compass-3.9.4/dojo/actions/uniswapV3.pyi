from dataclasses import dataclass
from decimal import Decimal
from dojo.actions.base_action import BaseAction as BaseAction
from dojo.agents.base_agent import BaseAgent as BaseAgent
from dojo.network.constants import ZERO_ADDRESS as ZERO_ADDRESS
from dojo.observations import UniswapV3Observation as UniswapV3Observation

BaseUniswapV3Action = BaseAction[UniswapV3Observation]
UniswapV3Action = BaseUniswapV3Action

@dataclass
class LowLevelUniswapV3Trade(BaseUniswapV3Action):
    pool: str
    quantities: tuple[Decimal, Decimal]
    sqrt_price_limit_x96: int | None = ...
    def __init__(self, pool, quantities, sqrt_price_limit_x96=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3Trade(BaseUniswapV3Action):
    pool: str
    quantities: tuple[Decimal, Decimal]
    price_limit: Decimal | None = ...
    def __init__(self, pool, quantities, price_limit=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3TradeToTickRange(BaseUniswapV3Action):
    pool: str
    quantities: tuple[Decimal, Decimal]
    tick_range: tuple[int, int]
    def __init__(self, pool, quantities, tick_range, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3Quote(BaseUniswapV3Action):
    pool: str
    quantities: tuple[Decimal, Decimal]
    tick_range: tuple[int, int]
    liquidity: int = ...
    owner: str = ...
    def __init__(self, pool, quantities, tick_range, liquidity=..., owner=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3ProvideLiquidity(BaseUniswapV3Action):
    pool: str
    tick_range: tuple[int, int]
    liquidity: int
    def __init__(self, pool, tick_range, liquidity, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3ProvideQuantities(BaseUniswapV3Action):
    pool: str
    tick_range: tuple[int, int]
    amount0: Decimal
    amount1: Decimal
    owner: str = ...
    auto_trade: bool = ...
    def __init__(self, pool, tick_range, amount0, amount1, owner=..., auto_trade=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3IncreaseLiquidity(BaseUniswapV3Action):
    pool: str
    position_id: int
    liquidity: int
    owner: str = ...
    def __init__(self, pool, position_id, liquidity, owner=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3WithdrawLiquidity(BaseUniswapV3Action):
    position_id: int
    liquidity: int
    owner: str = ...
    def __init__(self, position_id, liquidity, owner=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3LiquidatePosition(BaseUniswapV3Action):
    position_id: int
    def __init__(self, position_id, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3Collect(BaseUniswapV3Action):
    pool: str
    quantities: tuple[Decimal, Decimal]
    tick_range: tuple[int, int]
    def __init__(self, pool, quantities, tick_range, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3SetFeeProtocol(BaseUniswapV3Action):
    pool: str
    quantities: tuple[Decimal, Decimal]
    __annotations__ = ...
    def __init__(self, pool, quantities, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3CollectFull(BaseUniswapV3Action):
    pool: str
    position_id: str
    def __init__(self, pool, position_id, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class UniswapV3BurnNew(BaseUniswapV3Action):
    position_id: str
    def __init__(self, position_id, *, agent, gas=..., gas_price=...) -> None: ...
