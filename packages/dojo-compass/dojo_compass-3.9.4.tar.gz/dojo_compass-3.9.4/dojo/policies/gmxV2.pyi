import abc
from dojo.actions.gmxV2 import BaseGmxAction as BaseGmxAction
from dojo.agents import GmxV2Agent as GmxV2Agent
from dojo.observations import GmxV2Observation as GmxV2Observation
from dojo.policies.base_policy import BasePolicy as BasePolicy

class GmxV2Policy(BasePolicy[BaseGmxAction, GmxV2Agent, GmxV2Observation], metaclass=abc.ABCMeta): ...
