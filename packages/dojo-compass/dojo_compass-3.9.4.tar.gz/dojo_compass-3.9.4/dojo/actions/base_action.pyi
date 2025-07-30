from dataclasses import dataclass
from dojo.agents.base_agent import BaseAgent as BaseAgent
from dojo.observations import BaseObservation as BaseObservation
from typing import Generic, TypeVar

Observation = TypeVar('Observation', bound=BaseObservation)

@dataclass(kw_only=True)
class BaseAction(Generic[Observation]):
    agent: BaseAgent[Observation]
    gas: int | None = ...
    gas_price: int | None = ...
    def __init__(self, *, agent, gas=..., gas_price=...) -> None: ...
