from dataclasses import dataclass
from decimal import Decimal
from dojo.actions.base_action import BaseAction as BaseAction
from dojo.config.data.aave_config import BorrowingMode as BorrowingMode
from dojo.observations.aaveV3 import AAVEv3Observation as AAVEv3Observation

BaseAaveAction = BaseAction[AAVEv3Observation]

@dataclass
class AAVEv3Supply(BaseAaveAction):
    token: str
    amount: Decimal
    onBehalfOf: str | None = ...
    def __init__(self, token, amount, onBehalfOf=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3Withdraw(BaseAaveAction):
    token: str
    amount: Decimal
    user: str | None = ...
    to: str | None = ...
    def __init__(self, token, amount, user=..., to=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3WithdrawAll(BaseAaveAction):
    token: str
    def __init__(self, token, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3Borrow(BaseAaveAction):
    token: str
    amount: Decimal
    mode: BorrowingMode
    user: str | None = ...
    onBehalfOf: str | None = ...
    def __init__(self, token, amount, mode, user=..., onBehalfOf=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3BorrowToHealthFactor(BaseAaveAction):
    token: str
    factor: float
    mode: BorrowingMode
    def __init__(self, token, factor, mode, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3Repay(BaseAaveAction):
    token: str
    amount: Decimal
    mode: BorrowingMode
    user: str | None = ...
    def __init__(self, token, amount, mode, user=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3RepayAll(BaseAaveAction):
    token: str
    mode: BorrowingMode
    def __init__(self, token, mode, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3RepayToHealthFactor(BaseAaveAction):
    token: str
    factor: float
    mode: BorrowingMode
    def __init__(self, token, factor, mode, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3Liquidation(BaseAaveAction):
    collateral: str
    debt: str
    user: str
    debtToCover: int
    receiveAToken: bool = ...
    def __init__(self, collateral, debt, user, debtToCover, receiveAToken=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3FullLiquidation(BaseAaveAction):
    collateral: str
    debt: str
    user: str
    receiveAToken: bool = ...
    def __init__(self, collateral, debt, user, receiveAToken=..., *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3FlashLoanSimple(BaseAaveAction):
    token: str
    amount: Decimal
    receiver: str
    params: bytes
    def __init__(self, token, amount, receiver, params, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3FlashLoan(BaseAaveAction):
    tokens: list[str]
    amounts: list[Decimal]
    modes: list[BorrowingMode]
    receiver: str
    params: bytes | None
    def __init__(self, tokens, amounts, modes, receiver, params, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3MintToTreasury(BaseAaveAction):
    tokens: list[str]
    def __init__(self, tokens, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3SetUserUseReserveAsCollateral(BaseAaveAction):
    reserve: str
    useAsCollateral: bool
    user: str | None
    def __init__(self, reserve, useAsCollateral, user, *, agent, gas=..., gas_price=...) -> None: ...

@dataclass
class AAVEv3SetUserEMode(BaseAaveAction):
    user: str | None
    emode: int
    def __init__(self, user, emode, *, agent, gas=..., gas_price=...) -> None: ...
