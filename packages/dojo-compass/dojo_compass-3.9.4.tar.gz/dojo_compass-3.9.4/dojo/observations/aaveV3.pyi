from _typeshed import Incomplete
from dataclasses import dataclass
from decimal import Decimal
from dojo.config import cfg as cfg
from dojo.network import LiveBackend as LiveBackend
from dojo.network.base_backend import BaseBackend as BaseBackend
from dojo.network.forked_backend import ForkedBackend as ForkedBackend
from dojo.observations.base_observation import BaseObservation as BaseObservation
from typing import Any

@dataclass
class ReserveConfig:
    ltv: int
    liquidation_threshold: int
    liquidation_bonus: int
    decimals: int
    is_active: bool
    is_frozen: bool
    borrowing_enabled: bool
    stable_borrowing_enabled: bool
    asset_paused: bool
    borrowing_in_isolation_enabled: bool
    reserved: bool
    reserve_factor: int
    borrow_cap: int
    supply_cap: int
    liquidation_fee: int
    emode_category: int
    unbacked_mint_cap: int
    debt_ceiling: int
    def __init__(self, ltv, liquidation_threshold, liquidation_bonus, decimals, is_active, is_frozen, borrowing_enabled, stable_borrowing_enabled, asset_paused, borrowing_in_isolation_enabled, reserved, reserve_factor, borrow_cap, supply_cap, liquidation_fee, emode_category, unbacked_mint_cap, debt_ceiling) -> None: ...

@dataclass
class ReserveData:
    configuration: ReserveConfig
    liquidity_index: int
    current_liquidity_rate: int
    variable_borrow_index: int
    current_variable_borrow_rate: int
    current_stable_borrow_rate: int
    last_update_timestamp: int
    id: int
    atoken_address: str
    stable_debt_token_address: str
    variable_debt_token_address: str
    interest_rate_strategy_address: str
    accrued_to_treasury: int
    unbacked: int
    isolation_mode_total_debt: int
    def __init__(self, configuration, liquidity_index, current_liquidity_rate, variable_borrow_index, current_variable_borrow_rate, current_stable_borrow_rate, last_update_timestamp, id, atoken_address, stable_debt_token_address, variable_debt_token_address, interest_rate_strategy_address, accrued_to_treasury, unbacked, isolation_mode_total_debt) -> None: ...

@dataclass
class UserAccountData:
    totalCollateral: Decimal
    totalDebt: Decimal
    availableBorrows: Decimal
    currentLiquidationThreshold: float
    ltv: float
    healthFactor: float
    def __init__(self, totalCollateral, totalDebt, availableBorrows, currentLiquidationThreshold, ltv, healthFactor) -> None: ...

def split_configuration_data(config_int: int) -> ReserveConfig: ...

class AAVEv3Observation(BaseObservation):
    pools: Incomplete
    def __init__(self, backend: BaseBackend) -> None: ...
    def tokens(self) -> list[Any]: ...
    def market_agent_tokens(self) -> list[Any]: ...
    def balance(self, token_name: str, address: str) -> int: ...
    def get_asset_price(self, asset_name: str) -> int: ...
    def get_asset_prices(self, asset_names: list[str]) -> list[int]: ...
    def get_user_current_debt(self, agent_address: str, reserve_symbol: str) -> tuple[Decimal, Decimal]: ...
    def get_user_account_data_base(self, agent_address: str) -> UserAccountData: ...
    def get_user_account_data(self, agent_address: str, currency_name: str) -> UserAccountData: ...
    def events_last_blocks(self): ...
    def get_reserve_data(self, reserve_symbol: str) -> ReserveData: ...
