import abc
import numpy as np
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from dojo.actions.base_action import BaseAction as BaseAction
from dojo.agents import BaseAgent as BaseAgent
from dojo.common.constants import Chain as Chain
from dojo.network import BaseBackend as BaseBackend, ForkedBackend as ForkedBackend, LiveBackend as LiveBackend, LocalBackend as LocalBackend
from dojo.network.constants import MAX_UINT256 as MAX_UINT256
from dojo.observations import BaseObservation as BaseObservation
from numpy.typing import NDArray as NDArray
from typing import Any, Generator, Generic, Literal, TypeVar
from web3.contract.contract import Contract as Contract

Action = TypeVar('Action', bound=BaseAction[Any])
Observation = TypeVar('Observation', bound=BaseObservation)
logger: Incomplete

class BaseEnvironment(ABC, Generic[Action, Observation], metaclass=abc.ABCMeta):
    backend: BaseBackend
    obs: Observation
    rewards: NDArray[np.generic]
    port: Incomplete
    agents: Incomplete
    block_range: Incomplete
    ready_to_run_after_reset: bool
    def __init__(self, chain: Chain, agents: list[BaseAgent[Observation]], block_range: tuple[int, int] | None, backend_type: Literal['forked', 'local', 'live'] = 'forked', port: int | None = None, token_data: dict[str, dict[datetime, Decimal]] | None = None, market_agent_portfolio: dict[str, Decimal] | None = None) -> None: ...
    @property
    def chain(self) -> Chain: ...
    def deploy_forked_contract(self, env_name: str, contract_name: str) -> None: ...
    def deploy_local_contract(self, protocol: str, name: str, args: list[Any] = [], bytecode: str | None = None) -> Contract: ...
    @abstractmethod
    def setup_contracts_forked(self) -> list[str]: ...
    @abstractmethod
    def setup_contracts_local(self) -> list[str]: ...
    @abstractmethod
    def initialize_state(self) -> None: ...
    def reset(self) -> Observation: ...
    def iter_block(self, *, dashboard_server_port: int | None = None, batch_size: int = 0, status_bar: bool = False) -> Generator[int, None, None]: ...
    def step(self, actions: list[Action]) -> NDArray[np.generic]: ...
