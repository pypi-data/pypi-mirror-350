import abc
from dojo.agents.base_agent import BaseAgent as BaseAgent
from dojo.observations import GmxV2Observation as GmxV2Observation

class GmxV2Agent(BaseAgent[GmxV2Observation], metaclass=abc.ABCMeta): ...
