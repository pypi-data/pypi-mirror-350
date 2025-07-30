"""User exposed models for order creation on GMXv2."""
from dataclasses import dataclass
from decimal import Decimal

from dataclasses_json import LetterCase, dataclass_json

from dojo.actions.gmxV2.base_gmx_action import InternalBaseGmxAction as BaseGmxAction
from dojo.actions.gmxV2.orders.params import OrderType
from dojo.agents import BaseAgent
from dojo.observations.gmxV2 import GmxV2Observation


@dataclass
class OrderDef:
    """GmxOrder definition for GMX v2."""

    order_type: OrderType
    is_long: bool
    is_limit_order: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxBaseTraderOrder(BaseGmxAction):
    """Base class for trader orders on GMX v2."""

    agent: BaseAgent[GmxV2Observation]
    size_delta_usd: Decimal
    market_key: str
    token_in_symbol: str
    collateral_token_symbol: str
    observations: GmxV2Observation
    leverage: Decimal
    slippage: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxIncreaseLongMarketOrder(GmxBaseTraderOrder):
    """Action representing an increase long market order on GMX v2.

    :param agent: The agent executing the action.
    :param size_delta_usd: The size delta in USD.
    :param market_key: The market key.
    :param token_in_symbol: The token in symbol.
    :param collateral_token_symbol: The collateral token symbol.
    :param observations: The observations.
    :param leverage: The leverage.
    :param slippage: The slippage.
    :param gas: Optional gas units.
    :param gas_price: Optional gas price in wei.
    """

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxDecreaseLongMarketOrder(GmxBaseTraderOrder):
    """Action representing an decrease long market order on GMX v2.

    :param agent: The agent executing the action.
    :param size_delta_usd: The size delta in USD.
    :param market_key: The market key.
    :param token_in_symbol: The token in symbol.
    :param collateral_token_symbol: The collateral token symbol.
    :param observations: The observations.
    :param leverage: The leverage.
    :param slippage: The slippage.
    :param gas: Optional gas units.
    :param gas_price: Optional gas price in wei.
    """

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxIncreaseShortMarketOrder(GmxBaseTraderOrder):
    """Action representing an increase short market order on GMX v2.

    :param agent: The agent executing the action.
    :param size_delta_usd: The size delta in USD.
    :param market_key: The market key.
    :param token_in_symbol: The token in symbol.
    :param collateral_token_symbol: The collateral token symbol.
    :param observations: The observations.
    :param leverage: The leverage.
    :param slippage: The slippage.
    :param gas: Optional gas units.
    :param gas_price: Optional gas price in wei.
    """

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxDecreaseShortMarketOrder(GmxBaseTraderOrder):
    """Action representing an decrease short market order on GMX v2.

    :param agent: The agent executing the action.
    :param size_delta_usd: The size delta in USD.
    :param market_key: The market key.
    :param token_in_symbol: The token in symbol.
    :param collateral_token_symbol: The collateral token symbol.
    :param observations: The observations.
    :param leverage: The leverage.
    :param slippage: The slippage.
    :param gas: Optional gas units.
    :param gas_price: Optional gas price in wei.
    """

    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxIncreaseLongLimitOrder(GmxBaseTraderOrder):
    """Action representing an increase long limit order on GMX v2.

    :param agent: The agent executing the action.
    :param size_delta_usd: The size delta in USD.
    :param market_key: The market key.
    :param token_in_symbol: The token in symbol.
    :param collateral_token_symbol: The collateral token symbol.
    :param observations: The observations.
    :param leverage: The leverage.
    :param slippage: The slippage.
    :param trigger_price: The trigger price.
    :param gas: Optional gas units.
    :param gas_price: Optional gas price in wei.
    """

    trigger_price: Decimal


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxDecreaseLongLimitOrder(GmxBaseTraderOrder):
    """Action representing an decrease long limit order on GMX v2.

    :param agent: The agent executing the action.
    :param size_delta_usd: The size delta in USD.
    :param market_key: The market key.
    :param token_in_symbol: The token in symbol.
    :param collateral_token_symbol: The collateral token symbol.
    :param observations: The observations.
    :param leverage: The leverage.
    :param slippage: The slippage.
    :param trigger_price: The trigger price.
    :param gas: Optional gas units.
    :param gas_price: Optional gas price in wei.
    """

    trigger_price: Decimal


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxIncreaseShortLimitOrder(GmxBaseTraderOrder):
    """Action representing an increase short limit order on GMX v2.

    :param agent: The agent executing the action.
    :param size_delta_usd: The size delta in USD.
    :param market_key: The market key.
    :param token_in_symbol: The token in symbol.
    :param collateral_token_symbol: The collateral token symbol.
    :param observations: The observations.
    :param leverage: The leverage.
    :param slippage: The slippage.
    :param trigger_price: The trigger price.
    :param gas: Optional gas units.
    :param gas_price: Optional gas price in wei.
    """

    trigger_price: Decimal


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxDecreaseShortLimitOrder(GmxBaseTraderOrder):
    """Action representing a decrease short limit order on GMX v2.

    :param agent: The agent executing the action.
    :param size_delta_usd: The size delta in USD.
    :param market_key: The market key.
    :param token_in_symbol: The token in symbol.
    :param collateral_token_symbol: The collateral token symbol.
    :param observations: The observations.
    :param leverage: The leverage.
    :param slippage: The slippage.
    :param trigger_price: The trigger price.
    :param gas: Optional gas units.
    :param gas_price: Optional gas price in wei.
    """

    trigger_price: Decimal


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GmxSwapOrder(BaseGmxAction):
    """Action representing a swap order on GMX v2.

    :param agent: The agent executing the action.
    :param in_token: The input token.
    :param out_token: The output token.
    :param in_token_amount: The input token amount.
    :param slippage: The slippage.
    :param observations: The observations.
    :param gas: Optional gas units.
    :param gas_price: Optional gas price in wei.
    """

    in_token: str
    out_token: str
    in_token_amount: Decimal
    slippage: int
    observations: GmxV2Observation
