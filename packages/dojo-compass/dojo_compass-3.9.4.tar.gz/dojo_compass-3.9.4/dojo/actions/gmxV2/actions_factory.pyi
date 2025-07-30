from dojo.actions.gmxV2.deposit.models import GmxHistoricDeposit as GmxHistoricDeposit
from dojo.actions.gmxV2.keeper_actions.models import GmxHistoricExecuteDeposit as GmxHistoricExecuteDeposit, GmxHistoricExecuteOrder as GmxHistoricExecuteOrder, GmxHistoricExecuteWithdrawal as GmxHistoricExecuteWithdrawal, SetPricesParams as SetPricesParams
from dojo.actions.gmxV2.orders.base_models import GmxHistoricOrder as GmxHistoricOrder, GmxHistoricOrderCancel as GmxHistoricOrderCancel, GmxHistoricOrderUpdate as GmxHistoricOrderUpdate
from dojo.actions.gmxV2.orders.params import DecreasePositionSwapType as DecreasePositionSwapType, OrderType as OrderType
from dojo.actions.gmxV2.withdrawal.models import GmxHistoricWithdrawal as GmxHistoricWithdrawal
from dojo.agents.base_agent import BaseAgent as BaseAgent
from dojo.observations import GmxV2Observation as GmxV2Observation

DEFAULT_PROVIDER: str
