import abc
from dojo.actions.uniswapV3 import BaseUniswapV3Action as BaseUniswapV3Action
from dojo.agents import UniswapV3Agent as UniswapV3Agent
from dojo.observations import UniswapV3Observation as UniswapV3Observation
from dojo.policies.base_policy import BasePolicy as BasePolicy

class UniswapV3Policy(BasePolicy[BaseUniswapV3Action, UniswapV3Agent, UniswapV3Observation], metaclass=abc.ABCMeta): ...
