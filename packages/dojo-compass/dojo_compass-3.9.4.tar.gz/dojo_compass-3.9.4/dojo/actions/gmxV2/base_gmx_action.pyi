from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from dojo.actions.base_action import BaseAction as BaseAction
from dojo.observations import GmxV2Observation as GmxV2Observation

BaseGmxAction = BaseAction[GmxV2Observation]

@dataclass
class InternalBaseGmxAction(DataClassJsonMixin, BaseAction[GmxV2Observation]):
    def __init__(self, *generated_args, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...
