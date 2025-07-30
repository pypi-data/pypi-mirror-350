import abc
from abc import ABC, abstractmethod
from dojo.actions.base_action import BaseAction as BaseAction
from dojo.agents.base_agent import BaseAgent as BaseAgent
from dojo.observations import BaseObservation as BaseObservation
from typing import Any, Generic, TypeVar

Action = TypeVar('Action', bound=BaseAction[Any])
Agent = TypeVar('Agent', bound=BaseAgent[Any])
Observation = TypeVar('Observation', bound=BaseObservation)

class BasePolicy(ABC, Generic[Action, Agent, Observation], metaclass=abc.ABCMeta):
    agent: Agent
    def __init__(self) -> None: ...
    def fit(self, *args: Any, **kwargs: dict[str, Any]) -> Any: ...
    @abstractmethod
    def predict(self, obs: Observation) -> list[Action]: ...
