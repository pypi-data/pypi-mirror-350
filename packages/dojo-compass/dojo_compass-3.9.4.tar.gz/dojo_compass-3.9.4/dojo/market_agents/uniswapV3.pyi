import abc
from _typeshed import Incomplete
from dojo import money as money
from dojo.actions.uniswapV3 import LowLevelUniswapV3Trade as LowLevelUniswapV3Trade, UniswapV3Action as UniswapV3Action, UniswapV3Quote as UniswapV3Quote
from dojo.agents import BaseAgent as BaseAgent
from dojo.common.constants import Chain as Chain
from dojo.config import cfg as cfg
from dojo.dataloaders import UniswapV3Loader as UniswapV3Loader
from dojo.dataloaders.base_uniswapV3_loader import BaseUniswapV3Loader as BaseUniswapV3Loader
from dojo.dataloaders.formats import UniswapV3Burn as UniswapV3Burn, UniswapV3Mint as UniswapV3Mint, UniswapV3Swap as UniswapV3Swap
from dojo.network.constants import ZERO_ADDRESS as ZERO_ADDRESS
from dojo.observations.uniswapV3 import UniswapV3Observation as UniswapV3Observation
from dojo.policies import UniswapV3Policy as UniswapV3Policy
from typing import Any, Literal

class BaseMarketPolicy(UniswapV3Policy, metaclass=abc.ABCMeta):
    DEFAULT_GAS: int
    chain: Incomplete
    pools: Incomplete
    replay_events: Incomplete
    def __init__(self, chain: Chain, pools: list[str], block_range: tuple[int, int], dataloader: BaseUniswapV3Loader, mode: Literal['standard', 'swaps_only'] = 'standard') -> None: ...

class _HistoricReplayPolicy(BaseMarketPolicy):
    DEFAULT_GAS: int
    def __init__(self, chain: Chain, pools: list[str], block_range: tuple[int, int], dataloader: BaseUniswapV3Loader, mode: Literal['standard', 'swaps_only'] = 'standard') -> None: ...
    def predict(self, obs: UniswapV3Observation) -> list[UniswapV3Action]: ...

class HistoricReplayAgent(BaseAgent[UniswapV3Observation]):
    def __init__(self, chain: Chain, pools: list[str], block_range: tuple[int, int], mode: Literal['standard', 'swaps_only'] = 'standard', name: str = 'MarketAgent', Dataloader: type[BaseUniswapV3Loader] = ...) -> None: ...
    def reward(self, obs: Any) -> float: ...
