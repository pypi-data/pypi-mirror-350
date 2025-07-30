from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    date: datetime
    block: int
    log_index: int
    action: str
    gas: int
    gas_price: int
    __annotations__ = ...
    def __init__(self, date, block, log_index, action, gas, gas_price) -> None: ...

@dataclass
class UniswapV3Event(Event):
    date: datetime
    block: int
    log_index: int
    action: str
    pool: str
    gas: int
    gas_price: int
    __annotations__ = ...
    def __init__(self, date, block, log_index, action, gas, gas_price, pool) -> None: ...

@dataclass
class UniswapV3Initialize(UniswapV3Event):
    pool: str
    sqrt_priceX96: int
    tick: int
    __annotations__ = ...
    def __init__(self, date, block, log_index, action, gas, gas_price, pool, sqrt_priceX96, tick) -> None: ...

@dataclass
class UniswapV3Swap(UniswapV3Event):
    pool: str
    quantities: list[int]
    sqrt_price_limit_x96: int
    __annotations__ = ...
    def __init__(self, date, block, log_index, action, gas, gas_price, pool, quantities, sqrt_price_limit_x96) -> None: ...

@dataclass
class UniswapV3Mint(UniswapV3Event):
    pool: str
    quantities: list[int]
    tick_range: list[int]
    liquidity: int
    owner: str
    __annotations__ = ...
    def __init__(self, date, block, log_index, action, gas, gas_price, pool, quantities, tick_range, liquidity, owner) -> None: ...

@dataclass
class UniswapV3Burn(UniswapV3Event):
    pool: str
    quantities: list[int]
    tick_range: list[int]
    liquidity: int
    owner: str
    __annotations__ = ...
    def __init__(self, date, block, log_index, action, gas, gas_price, pool, quantities, tick_range, liquidity, owner) -> None: ...

@dataclass
class UniswapV3Collect(UniswapV3Event):
    pool: str
    quantities: list[int]
    tick_range: list[int]
    __annotations__ = ...
    def __init__(self, date, block, log_index, action, gas, gas_price, pool, quantities, tick_range) -> None: ...

@dataclass
class GMXEvent(Event):
    contract: str
    transaction_hash: str
    event_data: str
    inner_event_name: str
    topic1: str | None = ...
    topic2: str | None = ...
    def __init__(self, date, block, log_index, action, gas, gas_price, contract, transaction_hash, event_data, inner_event_name, topic1=..., topic2=...) -> None: ...
