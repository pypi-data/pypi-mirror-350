from _typeshed import Incomplete
from dataclasses import dataclass
from decimal import Decimal
from dojo.actions.aaveV3 import AAVEv3Borrow as AAVEv3Borrow, AAVEv3Liquidation as AAVEv3Liquidation, AAVEv3MintToTreasury as AAVEv3MintToTreasury, AAVEv3Repay as AAVEv3Repay, AAVEv3Supply as AAVEv3Supply, AAVEv3Withdraw as AAVEv3Withdraw, BaseAaveAction as BaseAaveAction
from dojo.agents import BaseAgent as BaseAgent
from dojo.common.constants import Chain as Chain
from dojo.config import cfg as cfg
from dojo.config.data.aave_config import BorrowingMode as BorrowingMode
from dojo.dataloaders import AaveV3Loader as AaveV3Loader
from dojo.money import get_decimals as get_decimals
from dojo.money.format import to_human_format as to_human_format
from dojo.observations.aaveV3 import AAVEv3Observation as AAVEv3Observation
from dojo.policies import AAVEv3Policy as BaseAAVEv3Policy
from typing import Any

logger: Incomplete

@dataclass
class _TokenAndAmount:
    token_name: str
    amount: Decimal
    def __init__(self, token_name, amount) -> None: ...

@dataclass
class _UserData:
    collaterals: list[_TokenAndAmount]
    borrows: list[_TokenAndAmount]
    def __init__(self, collaterals, borrows) -> None: ...

class _HistoricReplayPolicy(BaseAAVEv3Policy):
    DEFAULT_GAS: int
    AgentT = BaseAgent[AAVEv3Observation]
    chain: Incomplete
    block_range: Incomplete
    replay_events: Incomplete
    local_contracts: Incomplete
    def __init__(self, chain: Chain, block_range: tuple[int, int]) -> None: ...
    def predict(self, obs: AAVEv3Observation) -> list[BaseAaveAction]: ...

class HistoricReplayAgent(BaseAgent[Any]):
    def __init__(self, chain: Chain, block_range: tuple[int, int], name: str = 'MarketAgent') -> None: ...
    def reward(self, obs: Any) -> float: ...
