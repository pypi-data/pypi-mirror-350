from dataclasses import dataclass
from dojo.actions.base_action import BaseAction as BaseAction
from dojo.observations.base_observation import BaseObservation as BaseObservation
from typing import Generic, TypeVar

Observation = TypeVar('Observation', bound=BaseObservation)

@dataclass
class SleepAction(BaseAction[Observation], Generic[Observation]):
    number_of_blocks_to_sleep: int
    def __init__(self, number_of_blocks_to_sleep, *, agent, gas=..., gas_price=...) -> None: ...
