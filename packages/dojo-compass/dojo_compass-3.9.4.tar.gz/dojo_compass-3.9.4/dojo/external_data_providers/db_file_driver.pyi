from _typeshed import Incomplete
from dojo.actions.aaveV3 import AAVEv3BorrowToHealthFactor as AAVEv3BorrowToHealthFactor, AAVEv3RepayToHealthFactor as AAVEv3RepayToHealthFactor, AAVEv3Supply as AAVEv3Supply
from dojo.actions.uniswapV3 import UniswapV3Quote as UniswapV3Quote, UniswapV3Trade as UniswapV3Trade
from dojo.environments import AAVEv3Env as AAVEv3Env, GmxV2Env as GmxV2Env, UniswapV3Env as UniswapV3Env
from dojo.external_data_providers.protobuf.dashboard.v1.data_pb2 import AaveAction as AaveAction, AaveAgent as AaveAgent, AgentBlock as AgentBlock, BlockData as BlockData, GmxAction as GmxAction, GmxAgent as GmxAgent, GmxMarketData as GmxMarketData, Mode as Mode, Signal as Signal, TokenPairValues as TokenPairValues, UniswapAction as UniswapAction, UniswapPoolData as UniswapPoolData
from dojo.network import block_date as block_date
from dojo.observations import AAVEv3Observation as AAVEv3Observation, GmxV2Observation as GmxV2Observation, UniswapV3Observation as UniswapV3Observation
from dojo.utils.timings import state as state
from pathlib import Path

logger: Incomplete

class _DbFileDriver:
    start_time: Incomplete
    db_path: Incomplete
    env: Incomplete
    obs: Incomplete
    tokens: Incomplete
    simulation_title: Incomplete
    simulation_description: Incomplete
    mode: Incomplete
    conn: Incomplete
    cursor: Incomplete
    start_date: Incomplete
    end_date: Incomplete
    def __init__(self, env: UniswapV3Env | AAVEv3Env | GmxV2Env, obs: UniswapV3Observation | AAVEv3Observation | GmxV2Observation, output_file: Path, simulation_title: str, simulation_description: str, mode: Mode) -> None: ...
    def get_tokens(self, obs: UniswapV3Observation | AAVEv3Observation | GmxV2Observation) -> list[str]: ...
