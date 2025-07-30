from dojo.observations.uniswapV3 import *
from _typeshed import Incomplete
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from dojo.actions.uniswapV3 import LowLevelUniswapV3Trade as LowLevelUniswapV3Trade, UniswapV3Action as UniswapV3Action, UniswapV3BurnNew as UniswapV3BurnNew, UniswapV3Collect as UniswapV3Collect, UniswapV3CollectFull as UniswapV3CollectFull, UniswapV3ProvideLiquidity as UniswapV3ProvideLiquidity, UniswapV3ProvideQuantities as UniswapV3ProvideQuantities, UniswapV3Quote as UniswapV3Quote, UniswapV3SetFeeProtocol as UniswapV3SetFeeProtocol, UniswapV3Trade as UniswapV3Trade, UniswapV3TradeToTickRange as UniswapV3TradeToTickRange, UniswapV3WithdrawLiquidity as UniswapV3WithdrawLiquidity
from dojo.agents import BaseAgent as BaseAgent
from dojo.common.constants import Chain as Chain
from dojo.config import cfg as cfg
from dojo.dataloaders import UniswapV3Loader as UniswapV3Loader
from dojo.dataloaders.base_uniswapV3_loader import BaseUniswapV3Loader as BaseUniswapV3Loader
from dojo.dataloaders.formats import UniswapV3Event as UniswapV3Event
from dojo.environments.base_environments import BaseEnvironment as BaseEnvironment
from dojo.money.format import to_machine_format as to_machine_format
from dojo.network.constants import MAX_UINT256 as MAX_UINT256, ZERO_ADDRESS as ZERO_ADDRESS
from dojo.utils import disk_cache as disk_cache
from dojo.validations.single_sided_lp import validate_single_sided_lp as validate_single_sided_lp
from enum import Enum
from typing import Literal
from web3.types import PendingTx as PendingTx, TxReceipt as TxReceipt

logger: Incomplete

@dataclass
class _PoolInitState:
    sqrt_priceX96: int
    tick: int
    liquidity: int
    def __init__(self, sqrt_priceX96, tick, liquidity) -> None: ...

class UniswapV3MarketModelType(Enum):
    NO_MARKET = 'no_market'
    REPLAY = 'replay'
    REPLAY_TRADES_ONLY = 'replay_trades_only'

class UniswapV3Env(BaseEnvironment[UniswapV3Action, UniswapV3Observation]):
    POOL_SIZE: int
    MAX_SQRT_RATIO: int
    MIN_SQRT_RATIO: int
    MAX_TICK: int
    MIN_TICK: int
    AgentT = BaseAgent[UniswapV3Observation]
    dataloader: Incomplete
    obs: Incomplete
    pools: Incomplete
    def __init__(self, chain: Chain, agents: list[AgentT], pools: list[str], block_range: tuple[int, int], backend_type: Literal['forked', 'local', 'live'] = 'forked', port: int | None = None, token_data: dict[str, dict[datetime, Decimal]] | None = None, Dataloader: type[BaseUniswapV3Loader] = ...) -> None: ...
    def setup_contracts_local(self) -> list[str]: ...
    def initialize_state(self) -> None: ...
    def setup_contracts_forked(self) -> list[str]: ...
    def update_trading_volumes(self, pool: str, tokens: tuple[str, str], quantities: tuple[Decimal, Decimal]) -> None: ...
