from dojo.actions.gmxV2.deposit.models import GmxDeposit as GmxDeposit, GmxLPDeposit as GmxLPDeposit
from dojo.actions.gmxV2.deposit.params import CreateDepositParams as CreateDepositParams, CreateDepositParamsAddresses as CreateDepositParamsAddresses, CreateDepositParamsNumbers as CreateDepositParamsNumbers
from dojo.actions.gmxV2.orders.base_models import GmxOrder as GmxOrder
from dojo.actions.gmxV2.orders.models import GmxBaseTraderOrder as GmxBaseTraderOrder, GmxDecreaseLongLimitOrder as GmxDecreaseLongLimitOrder, GmxDecreaseLongMarketOrder as GmxDecreaseLongMarketOrder, GmxDecreaseShortLimitOrder as GmxDecreaseShortLimitOrder, GmxDecreaseShortMarketOrder as GmxDecreaseShortMarketOrder, GmxIncreaseLongLimitOrder as GmxIncreaseLongLimitOrder, GmxIncreaseLongMarketOrder as GmxIncreaseLongMarketOrder, GmxIncreaseShortLimitOrder as GmxIncreaseShortLimitOrder, GmxIncreaseShortMarketOrder as GmxIncreaseShortMarketOrder, GmxSwapOrder as GmxSwapOrder, OrderDef as OrderDef
from dojo.actions.gmxV2.orders.params import DecreasePositionSwapType as DecreasePositionSwapType, OrderType as OrderType
from dojo.actions.gmxV2.withdrawal.models import GmxLPWithdrawal as GmxLPWithdrawal, GmxWithdrawal as GmxWithdrawal
from dojo.config.deployments import get_address as get_address, get_decimals as get_decimals
from dojo.money.format import to_human_format as to_human_format, to_machine_format as to_machine_format
from dojo.network.constants import GMX_ORACLE_PRECISION as GMX_ORACLE_PRECISION, ZERO_ADDRESS as ZERO_ADDRESS

def deposit_adapter(lp_deposit: GmxDeposit, deposit_id: int) -> GmxLPDeposit: ...
def order_adapter(user_order: GmxBaseTraderOrder, order_id: int) -> GmxOrder: ...
def swap_adapter(swap: GmxSwapOrder, order_id: int) -> GmxOrder: ...
def withdrawal_adapter(withdrawal: GmxWithdrawal, withdrawal_id: int) -> GmxLPWithdrawal: ...
