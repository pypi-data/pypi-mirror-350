from dojo.actions.base_action import BaseAction as BaseAction
from dojo.observations import BaseObservation as BaseObservation
from dojo.policies.base_policy import BasePolicy as BasePolicy
from typing import Any

class DoNothingPolicy(BasePolicy[Any, Any, Any]):
    def __init__(self) -> None: ...
    def predict(self, obs: BaseObservation) -> list[BaseAction[Any]]: ...
