from _typeshed import Incomplete
from dojo.network.base_backend import BaseBackend as BaseBackend
from typing import Any
from web3.contract.contract import Contract as Contract

def generate_key(value: str) -> bytes: ...

ROLE_ADMIN: Incomplete
TIMELOCK_ADMIN: Incomplete
TIMELOCK_MULTISIG: Incomplete
CONFIG_KEEPER: Incomplete
LIMITED_CONFIG_KEEPER: Incomplete
CONTROLLER: Incomplete
GOV_TOKEN_CONTROLLER: Incomplete
ROUTER_PLUGIN: Incomplete
MARKET_KEEPER: Incomplete
FEE_KEEPER: Incomplete
FEE_DISTRIBUTION_KEEPER: Incomplete
ORDER_KEEPER: Incomplete
FROZEN_ORDER_KEEPER: Incomplete
PRICING_KEEPER: Incomplete
LIQUIDATION_KEEPER: Incomplete
ADL_KEEPER: Incomplete

def get_role_members(backend: BaseBackend, contract: Contract, role_key: bytes, start: int = 0, end: int = 15) -> Any: ...
def has_role(backend: BaseBackend, contract: Contract, account: str, roleKey: bytes) -> Any: ...
def grant_role(backend: BaseBackend, contract: Contract, account: str, roleKey: bytes, admin: str) -> None: ...
