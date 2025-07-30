from _typeshed import Incomplete
from dojo.actions import SleepAction as SleepAction
from dojo.actions.base_action import BaseAction as BaseAction
from dojo.actions.gmxV2.keeper_actions.models import GmxKeeperAction as GmxKeeperAction
from dojo.environments import AAVEv3Env as AAVEv3Env, UniswapV3Env as UniswapV3Env
from dojo.environments.gmxV2 import GmxV2Env as GmxV2Env
from dojo.external_data_providers.protobuf.dashboard.v1.data_pb2 import Mode as Mode
from dojo.network import ForkedBackend as ForkedBackend, LocalBackend as LocalBackend
from dojo.observations import AAVEv3Observation as AAVEv3Observation, GmxV2Observation as GmxV2Observation, UniswapV3Observation as UniswapV3Observation
from dojo.policies.base_policy import BasePolicy as BasePolicy
from typing import Literal

logger: Incomplete

def backtest_run(env: UniswapV3Env | AAVEv3Env | GmxV2Env, *, output_file: str | None = None, dashboard_server_port: int | None = None, transaction_order: Literal['in_order', 'fee'] = 'in_order', auto_close: bool = True, simulation_status_bar: bool = False, simulation_title: str = 'no title', simulation_description: str = 'no description') -> None: ...
