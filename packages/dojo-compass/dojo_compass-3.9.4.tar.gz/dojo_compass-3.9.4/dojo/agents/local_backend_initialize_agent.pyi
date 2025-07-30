from dojo.agents import BaseAgent as BaseAgent
from dojo.common import Chain as Chain
from dojo.policies import DoNothingPolicy as DoNothingPolicy
from typing import Any

class _LocalBackendInitializeAgent(BaseAgent[Any]):
    def __init__(self, chain: Chain, name: str = 'InitializeAgent') -> None: ...
    def reward(self, obs: Any) -> float: ...
