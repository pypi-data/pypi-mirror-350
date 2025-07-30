import abc
from dojo.actions.aaveV3 import BaseAaveAction as BaseAaveAction
from dojo.agents import AAVEv3Agent as AAVEv3Agent
from dojo.observations import AAVEv3Observation as AAVEv3Observation
from dojo.policies.base_policy import BasePolicy as BasePolicy

class AAVEv3Policy(BasePolicy[BaseAaveAction, AAVEv3Agent, AAVEv3Observation], metaclass=abc.ABCMeta):
    agent: AAVEv3Agent
