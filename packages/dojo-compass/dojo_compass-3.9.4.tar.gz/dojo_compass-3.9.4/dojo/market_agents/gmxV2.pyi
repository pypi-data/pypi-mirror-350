from _typeshed import Incomplete
from dojo.actions.gmxV2.base_gmx_action import BaseGmxAction as BaseGmxAction
from dojo.actions.gmxV2.keeper_actions.models import GmxExecuteOrder as GmxExecuteOrder
from dojo.agents import BaseAgent as BaseAgent
from dojo.common.constants import Chain as Chain
from dojo.dataloaders.gmx_loader import GMXLoader as GMXLoader
from dojo.models.gmxV2.limit_order import LimitOrderDefinitionHeap as LimitOrderDefinitionHeap
from dojo.models.gmxV2.market import MarketVenue as MarketVenue
from dojo.observations.gmxV2 import GmxV2Observation as GmxV2Observation
from dojo.policies import BasePolicy as BasePolicy
from typing import Any

class _HistoricReplayPolicy(BasePolicy[Any, Any, Any]):
    DEFAULT_GAS: int
    AgentT = BaseAgent[GmxV2Observation]
    chain: Incomplete
    block_range: Incomplete
    execution_delay: Incomplete
    market_venues: Incomplete
    replay_events: Incomplete
    original_key_to_action: Incomplete
    key_to_timestamp: Incomplete
    wnt_address: Incomplete
    original_key_to_actual_key: Incomplete
    lte_limit_orders: Incomplete
    gte_limit_orders: Incomplete
    order_id: int
    deposit_id: int
    withdrawal_id: int
    def __init__(self, chain: Chain, block_range: tuple[int, int], market_venues: list[MarketVenue], execution_delay: int = 10) -> None: ...
    def check_limit_orders_and_add_keeper_actions(self, obs: Any) -> list[GmxExecuteOrder]: ...
    def predict(self, obs: Any) -> list[Any]: ...

class HistoricReplayAgent(BaseAgent[Any]):
    def __init__(self, chain: Chain, block_range: tuple[int, int], market_venues: list[MarketVenue], name: str = 'MarketAgent') -> None: ...
    def reward(self, obs: Any) -> float: ...
