from _typeshed import Incomplete
from datetime import datetime
from decimal import Decimal
from dojo.actions.gmxV2.adapters import deposit_adapter as deposit_adapter, order_adapter as order_adapter, swap_adapter as swap_adapter, withdrawal_adapter as withdrawal_adapter
from dojo.actions.gmxV2.base_gmx_action import BaseGmxAction as BaseGmxAction
from dojo.actions.gmxV2.deposit.models import GmxDeposit as GmxDeposit, GmxDepositBase as GmxDepositBase, GmxHistoricDeposit as GmxHistoricDeposit, GmxLPDeposit as GmxLPDeposit
from dojo.actions.gmxV2.keeper_actions.models import GmxExecuteDeposit as GmxExecuteDeposit, GmxExecuteOrder as GmxExecuteOrder, GmxExecuteWithdrawal as GmxExecuteWithdrawal, GmxHistoricExecuteDeposit as GmxHistoricExecuteDeposit, GmxHistoricExecuteOrder as GmxHistoricExecuteOrder, GmxHistoricExecuteWithdrawal as GmxHistoricExecuteWithdrawal, GmxKeeperAction as GmxKeeperAction
from dojo.actions.gmxV2.orders.base_models import GmxCancelOrder as GmxCancelOrder, GmxHistoricOrder as GmxHistoricOrder, GmxHistoricOrderCancel as GmxHistoricOrderCancel, GmxHistoricOrderUpdate as GmxHistoricOrderUpdate, GmxOrder as GmxOrder, GmxUpdateOrder as GmxUpdateOrder
from dojo.actions.gmxV2.orders.models import GmxBaseTraderOrder as GmxBaseTraderOrder, GmxDecreaseLongLimitOrder as GmxDecreaseLongLimitOrder, GmxDecreaseLongMarketOrder as GmxDecreaseLongMarketOrder, GmxDecreaseShortLimitOrder as GmxDecreaseShortLimitOrder, GmxDecreaseShortMarketOrder as GmxDecreaseShortMarketOrder, GmxIncreaseLongLimitOrder as GmxIncreaseLongLimitOrder, GmxIncreaseLongMarketOrder as GmxIncreaseLongMarketOrder, GmxIncreaseShortLimitOrder as GmxIncreaseShortLimitOrder, GmxIncreaseShortMarketOrder as GmxIncreaseShortMarketOrder, GmxSwapOrder as GmxSwapOrder
from dojo.actions.gmxV2.orders.params import OrderType as OrderType
from dojo.actions.gmxV2.withdrawal.models import GmxHistoricWithdrawal as GmxHistoricWithdrawal, GmxLPWithdrawal as GmxLPWithdrawal, GmxWithdrawal as GmxWithdrawal, GmxWithdrawalBase as GmxWithdrawalBase
from dojo.agents import BaseAgent as BaseAgent
from dojo.common.constants import Chain as Chain
from dojo.config import cfg as cfg
from dojo.environments.base_environments import BaseEnvironment as BaseEnvironment
from dojo.market_agents.gmxV2 import HistoricReplayAgent as HistoricReplayAgent
from dojo.models.gmxV2.limit_order import LimitOrderDefinition as LimitOrderDefinition, LimitOrderDefinitionHeap as LimitOrderDefinitionHeap, LimitOrderOperator as LimitOrderOperator
from dojo.models.gmxV2.market import MarketVenue as MarketVenue
from dojo.models.gmxV2.position import ORACLE_DECIMALS as ORACLE_DECIMALS
from dojo.money.format import to_human_format as to_human_format
from dojo.network.constants import ZERO_ADDRESS as ZERO_ADDRESS
from dojo.observations.gmxV2 import GmxV2Observation as GmxV2Observation
from dojo.utils.debug_errors import debug_gmx_error as debug_gmx_error
from dojo.utils.gmxV2.token_utils import get_request_expiration_time as get_request_expiration_time
from enum import Enum
from typing import Literal
from web3.types import PendingTx as PendingTx, TxReceipt as TxReceipt

logger: Incomplete

class Vault(Enum):
    DEPOSIT = 'DepositVault'
    ORDER = 'OrderVault'
    WITHDRAWAL = 'WithdrawalVault'

class GmxV2MarketModelType(Enum):
    NO_MARKET = 'no_market'
    REPLAY = 'replay'

class GmxV2Env(BaseEnvironment[BaseGmxAction, GmxV2Observation]):
    AgentT = BaseAgent[GmxV2Observation]
    market_venues: Incomplete
    obs: Incomplete
    key_to_timestamp: Incomplete
    wnt_address: Incomplete
    execution_delay: Incomplete
    block_to_keeper_action: Incomplete
    original_key_to_actual_key: Incomplete
    lte_limit_orders: Incomplete
    gte_limit_orders: Incomplete
    action_to_method: Incomplete
    action_to_preprocess: Incomplete
    order_id: int
    deposit_id: int
    withdrawal_id: int
    def __init__(self, chain: Chain, agents: list[AgentT], block_range: tuple[int, int], market_venues: list[MarketVenue], market_impact: Literal['replay', 'no_market'] = 'no_market', backend_type: Literal['forked', 'local', 'live'] = 'forked', port: int | None = None, token_data: dict[str, dict[datetime, Decimal]] | None = None, execution_delay: int = 10) -> None: ...
    def reset(self) -> GmxV2Observation: ...
    def initialize_state(self) -> None: ...
    def setup_contracts_local(self) -> list[str]: ...
    def setup_contracts_forked(self) -> list[str]: ...
    def preprocess_actions(self, actions: list[BaseGmxAction]) -> list[BaseGmxAction]: ...
