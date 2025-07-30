from decimal import Decimal
from dojo.agents.base_agent import BaseAgent as BaseAgent
from dojo.observations import BaseObservation as BaseObservation
from typing import Any

class DummyAgent(BaseAgent[Any]):
    def __init__(self, policy: Any, initial_portfolio: dict[str, Decimal] | None = None, name: str = 'DummyAgent') -> None: ...
    def reward(self, obs: BaseObservation) -> float: ...
