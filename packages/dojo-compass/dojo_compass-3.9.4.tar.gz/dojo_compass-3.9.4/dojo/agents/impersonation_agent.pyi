from _typeshed import Incomplete
from dojo.agents.base_agent import BaseAgent as BaseAgent
from typing import Any

logger: Incomplete

class MonitoringAgent(BaseAgent[Any]):
    unit_token: Incomplete
    impersonation_address: Incomplete
    def __init__(self, impersonation_address: str, unit_token: str, policy: Any, name: str | None = None) -> None: ...
    def reward(self, obs: Any) -> float: ...
    def setup_live(self) -> None: ...
