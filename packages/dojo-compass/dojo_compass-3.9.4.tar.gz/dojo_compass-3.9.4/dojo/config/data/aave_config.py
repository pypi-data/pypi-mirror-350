"""Aave configuration data."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional

aave_supported_tokens = ["USDC", "WBTC", "USDT", "DAI", "WETH", "UNI", "BAL", "LDO"]


class BorrowingMode(Enum):
    """Borrowing mode for AAVE."""

    NONE = 0
    STABLE = 1
    VARIABLE = 2


@dataclass
class _RateStrategy:
    name: str
    optimalUsageRatio: int
    baseVariableBorrowRate: int
    variableRateSlope1: int
    variableRateSlope2: int
    stableRateSlope1: int
    stableRateSlope2: int
    baseStableRateOffset: int
    stableRateExcessOffset: int
    optimalStableToTotalDebtRatio: int


@dataclass
class _Strategy:
    baseLTVAsCollateral: int
    liquidationThreshold: int
    liquidationBonus: int
    liquidationProtocolFee: int
    borrowingEnabled: bool
    stableBorrowRateEnabled: bool
    flashLoanEnabled: bool
    reserveDecimals: int
    aTokenImpl: str
    reserveFactor: int
    supplyCap: int
    borrowCap: int
    debtCeiling: int
    borrowableIsolation: bool
    rateStrategyAddress: str = ""


@dataclass
class _Reserve:
    DAI: Optional[_Strategy] = None
    USDC: Optional[_Strategy] = None
    WBTC: Optional[_Strategy] = None
    WETH: Optional[_Strategy] = None
    USDT: Optional[_Strategy] = None
    UNI: Optional[_Strategy] = None
    BAL: Optional[_Strategy] = None
    LDO: Optional[_Strategy] = None


strategyDAI: _Strategy = _Strategy(
    baseLTVAsCollateral=7500,
    liquidationThreshold=8000,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=True,
    flashLoanEnabled=True,
    reserveDecimals=18,
    aTokenImpl="aDAI",
    reserveFactor=1000,
    supplyCap=2000000000,
    borrowCap=0,
    debtCeiling=0,
    borrowableIsolation=True,
)

strategyUSDC: _Strategy = _Strategy(
    baseLTVAsCollateral=8000,
    liquidationThreshold=8500,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=True,
    flashLoanEnabled=True,
    reserveDecimals=6,
    aTokenImpl="aUSDC",
    reserveFactor=1000,
    supplyCap=2000000000,
    borrowCap=0,
    debtCeiling=0,
    borrowableIsolation=True,
)

strategyWETH: _Strategy = _Strategy(
    baseLTVAsCollateral=8000,
    liquidationThreshold=8250,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=False,
    flashLoanEnabled=True,
    reserveDecimals=18,
    aTokenImpl="aWETH",
    reserveFactor=1000,
    supplyCap=0,
    borrowCap=0,
    debtCeiling=0,
    borrowableIsolation=False,
)

strategyWBTC: _Strategy = _Strategy(
    baseLTVAsCollateral=7000,
    liquidationThreshold=7500,
    liquidationBonus=11000,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=False,
    flashLoanEnabled=True,
    reserveDecimals=8,
    aTokenImpl="aWBTC",
    reserveFactor=2000,
    supplyCap=0,
    borrowCap=0,
    debtCeiling=0,
    borrowableIsolation=False,
)

strategyUSDT: _Strategy = _Strategy(
    baseLTVAsCollateral=7500,
    liquidationThreshold=8000,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=True,
    flashLoanEnabled=True,
    reserveDecimals=6,
    aTokenImpl="aUSDT",
    reserveFactor=1000,
    supplyCap=2000000000,
    borrowCap=0,
    debtCeiling=500000000,
    borrowableIsolation=True,
)

strategyUNI: _Strategy = _Strategy(
    baseLTVAsCollateral=7500,
    liquidationThreshold=8000,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=True,
    flashLoanEnabled=True,
    reserveDecimals=6,
    aTokenImpl="aUNI",
    reserveFactor=1000,
    supplyCap=2000000000,
    borrowCap=0,
    debtCeiling=500000000,
    borrowableIsolation=True,
)

strategyBAL: _Strategy = _Strategy(
    baseLTVAsCollateral=7500,
    liquidationThreshold=8000,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=True,
    flashLoanEnabled=True,
    reserveDecimals=6,
    aTokenImpl="aBAL",
    reserveFactor=1000,
    supplyCap=2000000000,
    borrowCap=0,
    debtCeiling=500000000,
    borrowableIsolation=True,
)

strategyLDO: _Strategy = _Strategy(
    baseLTVAsCollateral=7500,
    liquidationThreshold=8000,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=True,
    flashLoanEnabled=True,
    reserveDecimals=6,
    aTokenImpl="aLDO",
    reserveFactor=1000,
    supplyCap=2000000000,
    borrowCap=0,
    debtCeiling=500000000,
    borrowableIsolation=True,
)

defaultStrategy: _Strategy = _Strategy(
    baseLTVAsCollateral=7500,
    liquidationThreshold=8000,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=True,
    flashLoanEnabled=True,
    reserveDecimals=18,
    aTokenImpl="AToken",
    reserveFactor=1000,
    supplyCap=2000000000,
    borrowCap=0,
    debtCeiling=500000000,
    borrowableIsolation=True,
)
