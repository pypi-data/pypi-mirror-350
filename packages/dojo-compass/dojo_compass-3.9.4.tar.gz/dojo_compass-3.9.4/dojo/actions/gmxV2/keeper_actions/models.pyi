from dataclasses import dataclass
from dojo.actions.gmxV2.base_gmx_action import InternalBaseGmxAction as BaseGmxAction

@dataclass
class SetPricesParams:
    tokens: list[str]
    providers: list[str]
    data: list[dict[str, int]]
    def __init__(self, tokens, providers, data) -> None: ...

@dataclass
class GmxKeeperAction(BaseGmxAction):
    key: str
    block: int
    def __init__(self, *generated_args, key, block, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxExecuteOrderProfobufMixin:
    order_id: int
    def get_proto_args(self) -> dict[str, str | int]: ...
    def __init__(self, order_id) -> None: ...

@dataclass
class GmxExecuteDepositProfobufMixin:
    deposit_id: int
    def get_proto_args(self) -> dict[str, str | int]: ...
    def __init__(self, deposit_id) -> None: ...

@dataclass
class GmxExecuteWithdrawalProfobufMixin:
    withdrawal_id: int
    def get_proto_args(self) -> dict[str, str | int]: ...
    def __init__(self, withdrawal_id) -> None: ...

@dataclass
class GmxExecuteOrder(GmxKeeperAction, GmxExecuteOrderProfobufMixin):
    def __init__(self, *generated_args, order_id, key, block, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxExecuteDeposit(GmxKeeperAction, GmxExecuteDepositProfobufMixin):
    def __init__(self, *generated_args, deposit_id, key, block, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxExecuteWithdrawal(GmxKeeperAction, GmxExecuteWithdrawalProfobufMixin):
    def __init__(self, *generated_args, withdrawal_id, key, block, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxHistoricExecuteOrder(GmxKeeperAction):
    def __init__(self, *generated_args, key, block, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxHistoricExecuteDeposit(GmxKeeperAction):
    def __init__(self, *generated_args, key, block, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...

@dataclass
class GmxHistoricExecuteWithdrawal(GmxKeeperAction):
    def __init__(self, *generated_args, key, block, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...
