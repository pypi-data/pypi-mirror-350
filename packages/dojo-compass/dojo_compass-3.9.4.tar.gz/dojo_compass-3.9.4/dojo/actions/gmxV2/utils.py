"""Utilities for GMX actions."""
from decimal import Decimal
from typing import Any, Optional

from dojo.actions.gmxV2.orders.params import OrderType
from dojo.agents import BaseAgent
from dojo.models.gmxV2.market import Market, _get_gmx_markets
from dojo.network.constants import ZERO_ADDRESS
from dojo.observations.gmxV2 import GmxV2Observation
from dojo.utils.gmxV2.keys import (
    DECREASE_ORDER_GAS_LIMIT,
    DEPOSIT_GAS_LIMIT,
    EXECUTION_GAS_FEE_BASE_AMOUNT_V2_1,
    EXECUTION_GAS_FEE_MULTIPLIER_FACTOR,
    INCREASE_ORDER_GAS_LIMIT,
    SINGLE_SWAP_GAS_LIMIT,
    SWAP_ORDER_GAS_LIMIT,
    WITHDRAWAL_GAS_LIMIT,
)


def _get_swap_path(
    agent: BaseAgent[Any], in_token: str, out_token: str
) -> tuple[list[str], bool]:  # TODO(aidar) type annotations
    """Returns the swap path for the given in and out tokens.

    And whether the swap is multiswap, ie requires more than 1 market.
    """
    market_key_to_market = _get_gmx_markets(chain=agent.backend.chain)
    if in_token == "USDC":
        # if index token == out_token, then get the address of the market token
        for _, market in market_key_to_market.items():
            if market.index_token.symbol == out_token:
                gmx_market_address = market.market_token.address
    else:
        if in_token == "WBTC":
            in_token = "BTC"
        # if index token == in_token, then get the address of the market token
        for _, market in market_key_to_market.items():
            if market.index_token.symbol == in_token:
                gmx_market_address = market.market_token.address

    is_requires_multi_swap = False

    if (
        out_token != "USDC" and in_token != "USDC"
    ):  # if in and out tokens are not USDC, it requires multi swap
        is_requires_multi_swap = True
        if out_token == "WBTC":
            out_token = "BTC"
        # if index token == out_token, then get the address of the market token
        for _, market in market_key_to_market.items():
            if market.index_token.symbol == out_token:
                second_gmx_market_address = market.market_token.address

        return [
            gmx_market_address,
            second_gmx_market_address,
        ], is_requires_multi_swap

    return [gmx_market_address], is_requires_multi_swap


def _calculate_execution_fee(
    agent: BaseAgent[Any],
    order_type: Optional[OrderType] = None,
    deposit: bool = False,
    withdraw: bool = False,
) -> int:
    # TODO(aidar-call) refactor
    datastore = agent.backend.get_contract("DataStore")
    gas_limits = {
        "deposit": datastore.functions.getUint(DEPOSIT_GAS_LIMIT),
        "withdraw": datastore.functions.getUint(WITHDRAWAL_GAS_LIMIT),
        "single_swap": datastore.functions.getUint(SINGLE_SWAP_GAS_LIMIT),
        "swap_order": datastore.functions.getUint(SWAP_ORDER_GAS_LIMIT),
        "increase_order": datastore.functions.getUint(INCREASE_ORDER_GAS_LIMIT),
        "decrease_order": datastore.functions.getUint(DECREASE_ORDER_GAS_LIMIT),
        "estimated_fee_base_gas_limit": datastore.functions.getUint(
            EXECUTION_GAS_FEE_BASE_AMOUNT_V2_1
        ),
        "estimated_fee_multiplier_factor": datastore.functions.getUint(
            EXECUTION_GAS_FEE_MULTIPLIER_FACTOR
        ),
    }

    base_gas_limit = gas_limits["estimated_fee_base_gas_limit"].call()
    multiplier_factor = gas_limits["estimated_fee_multiplier_factor"].call()
    if deposit is True:
        order_function = gas_limits["deposit"]
    elif withdraw is True:
        order_function = gas_limits["withdraw"]
    elif order_type is OrderType.MARKET_SWAP:
        order_function = gas_limits["swap_order"]
    elif (
        order_type is OrderType.MARKET_INCREASE
        or order_type is OrderType.LIMIT_INCREASE
    ):
        order_function = gas_limits["increase_order"]
    elif (
        order_type is OrderType.MARKET_DECREASE
        or order_type is OrderType.LIMIT_DECREASE
    ):
        order_function = gas_limits["decrease_order"]
    adjusted_gas_limit = base_gas_limit + (
        order_function.call() * multiplier_factor / 10**30
    )

    execution_fee = adjusted_gas_limit * agent.backend.web3.eth.gas_price

    if order_type is OrderType.MARKET_SWAP:
        execution_fee = execution_fee * 1.5
    else:
        execution_fee = execution_fee * 1.2

    return int(execution_fee)


def _get_initial_collateral_delta_amount(
    size_delta_usd: Decimal,
    leverage: Decimal,
    collateral_token_symbol: str,
    observations: GmxV2Observation,
) -> Decimal:
    """Calculate the initial collateral delta amount."""
    collateral_price_usd = observations.get_token_price_by_token_symbol(
        collateral_token_symbol
    )
    return size_delta_usd / (leverage * collateral_price_usd)


def _get_acceptable_price(
    market_key: str,
    order_type: OrderType,
    is_long: bool,
    slippage: int,
    observations: GmxV2Observation,
) -> Decimal:
    """Calculate the acceptable price for the order."""
    market_price = observations.index_token_price(market_key)

    if (
        order_type is OrderType.MARKET_INCREASE
        or order_type is OrderType.LIMIT_INCREASE
    ):
        if is_long:
            return market_price * Decimal(1 + slippage / 10000)
        return market_price * Decimal(1 - slippage / 10000)
    elif (
        order_type is OrderType.MARKET_DECREASE
        or order_type is OrderType.LIMIT_DECREASE
    ):
        if is_long:
            return market_price * Decimal(1 - slippage / 10000)
        return market_price * Decimal(1 + slippage / 10000)
    return Decimal(0)


def _get_estimated_swap_output(
    agent: BaseAgent[Any],
    market: Market,
    obs: GmxV2Observation,
    in_token: str,
    amount: int,
) -> tuple[int, int]:  # out_token_amount, price_impact_usd
    reader_contract = agent.backend.get_contract("Reader")
    oracle_prices = obs._get_oracle_prices()
    index_token_prices = obs._get_value_or_raise(
        oracle_prices, market.index_token.address
    )
    long_token_prices = obs._get_value_or_raise(
        oracle_prices, market.long_token.address
    )
    short_token_prices = obs._get_value_or_raise(
        oracle_prices, market.short_token.address
    )
    output = agent.backend.contract_call(
        reader_contract.functions.getSwapAmountOut,
        (
            agent.backend.name2address["DataStore"],
            (
                market.market_token.address,
                market.index_token.address,
                market.long_token.address,
                market.short_token.address,
            ),
            (
                (
                    index_token_prices.data[0]["maxPrice"],
                    index_token_prices.data[0]["minPrice"],
                ),
                (
                    long_token_prices.data[0]["maxPrice"],
                    long_token_prices.data[0]["minPrice"],
                ),
                (
                    short_token_prices.data[0]["maxPrice"],
                    short_token_prices.data[0]["minPrice"],
                ),
            ),
            agent.backend.name2address[in_token],
            amount,
            ZERO_ADDRESS,  # ui_fee_receiver
        ),
    )
    return output[0], output[1]  # out_token_amount, price_impact_usd


def _get_long_token_amount(
    long_token_usd: Decimal,
    observations: GmxV2Observation,
    initial_long_token_symbol: str,
) -> Decimal:
    long_token_price = observations.get_token_price_by_token_symbol(
        initial_long_token_symbol
    )
    return long_token_usd / long_token_price


def _get_short_token_amount(
    short_token_usd: Decimal,
    observations: GmxV2Observation,
    initial_short_token_symbol: str,
) -> Decimal:
    short_token_price = observations.get_token_price_by_token_symbol(
        initial_short_token_symbol
    )
    return short_token_usd / short_token_price
