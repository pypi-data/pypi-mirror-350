"""Set of functions to get parameters for interaction with GMX contracts."""
from typing import Any

from hexbytes import HexBytes

from dojo.actions.gmxV2.deposit.models import GmxDepositBase
from dojo.actions.gmxV2.keeper_actions.models import SetPricesParams
from dojo.actions.gmxV2.orders.base_models import GmxOrder, GmxUpdateOrder
from dojo.actions.gmxV2.orders.params import (
    CreateOrderParamsAddresses,
    CreateOrderParamsNumbers,
)
from dojo.actions.gmxV2.withdrawal.models import GmxWithdrawalBase


def _get_update_order_args(order_action: GmxUpdateOrder) -> list[Any]:
    """Return arguments to encode in `updateOrder` function."""
    return [
        HexBytes(f"0x{order_action.key}"),
        order_action.size_delta_usd,
        order_action.acceptable_price,
        order_action.trigger_price,
        order_action.min_output_amount,
        order_action.auto_cancel,
    ]


def _get_create_withdrawal_args(withdrawal_action: GmxWithdrawalBase) -> list[Any]:
    """Return arguments to encode in `createWithdrawal` function."""
    return [
        withdrawal_action.create_withdrawal_params.receiver,
        withdrawal_action.create_withdrawal_params.callback_contract,
        withdrawal_action.create_withdrawal_params.ui_fee_receiver,
        withdrawal_action.create_withdrawal_params.market,
        withdrawal_action.create_withdrawal_params.long_token_swap_path,
        withdrawal_action.create_withdrawal_params.short_token_swap_path,
        withdrawal_action.create_withdrawal_params.min_long_token_amount,
        withdrawal_action.create_withdrawal_params.min_short_token_amount,
        withdrawal_action.create_withdrawal_params.should_unwrap_native_token,
        withdrawal_action.create_withdrawal_params.execution_fee,
        withdrawal_action.create_withdrawal_params.callback_gas_limit,
    ]


def _get_create_deposit_args(deposit_action: GmxDepositBase) -> list[Any]:
    """Return arguments to encode in `createDeposit` function."""
    return [
        deposit_action.create_deposit_params.addresses.receiver,
        deposit_action.create_deposit_params.addresses.callback_contract,
        deposit_action.create_deposit_params.addresses.ui_fee_receiver,
        deposit_action.create_deposit_params.addresses.market,
        deposit_action.create_deposit_params.addresses.initial_long_token,
        deposit_action.create_deposit_params.addresses.initial_short_token,
        deposit_action.create_deposit_params.addresses.long_token_swap_path,
        deposit_action.create_deposit_params.addresses.short_token_swap_path,
        deposit_action.create_deposit_params.numbers.min_market_tokens,
        deposit_action.create_deposit_params.should_unwrap_native_token,
        deposit_action.create_deposit_params.numbers.execution_fee,
        deposit_action.create_deposit_params.numbers.callback_gas_limit,
    ]


def _get_create_order_args_addresses(
    order_action_addresses: CreateOrderParamsAddresses,
) -> tuple[str, str, str, str, str | None, str | None, list[str]]:
    return (
        order_action_addresses.receiver,
        order_action_addresses.cancellation_receiver,
        order_action_addresses.callback_contract,
        order_action_addresses.ui_fee_receiver,
        order_action_addresses.market,
        order_action_addresses.initial_collateral_token,
        order_action_addresses.swap_path or [],
    )


def _get_create_order_args_numbers(
    order_action_numbers: CreateOrderParamsNumbers,
) -> tuple[int, int, int, int, int, int, int]:
    return (
        order_action_numbers.size_delta_usd,
        order_action_numbers.initial_collateral_delta_amount,
        order_action_numbers.trigger_price,
        order_action_numbers.acceptable_price,
        order_action_numbers.execution_fee,
        order_action_numbers.callback_gas_limit,
        order_action_numbers.min_output_amount,
    )


def _get_create_order_args(
    order_action: GmxOrder,
) -> tuple[
    tuple[
        str, str, str, str, str | None, str | None, list[str]
    ],  # TODO(aidar) Better return types
    tuple[int, int, int, int, int, int, int],
    int,
    int,
    bool,
    bool,
    bool,
    HexBytes,
]:
    """Return arguments to encode in `createOrder` function."""
    addresses = _get_create_order_args_addresses(
        order_action.create_order_params.addresses
    )
    numbers = _get_create_order_args_numbers(order_action.create_order_params.numbers)
    return (
        addresses,
        numbers,
        order_action.create_order_params.order_type.value,
        order_action.create_order_params.decrease_position_swap_type.value,
        order_action.create_order_params.is_long,
        order_action.create_order_params.should_unwrap_native_token,
        order_action.create_order_params.autoCancel,
        HexBytes(order_action.create_order_params.referral_code),
    )


def _get_set_prices(
    set_prices_params_list: list[SetPricesParams],
    update_at_timestamp: int,
    expiration_time: int,
) -> tuple[list[str], list[tuple[int, int]], int, int]:
    """Return arguments to encode in `setPrices` function."""
    tokens = [spp.tokens[0] for spp in set_prices_params_list]
    prices = [
        (spp.data[0]["minPrice"], spp.data[0]["maxPrice"])
        for spp in set_prices_params_list
    ]
    min_timestamp = update_at_timestamp + 1
    max_timestamp = update_at_timestamp + expiration_time - 1
    return (
        tokens,
        prices,
        min_timestamp,
        max_timestamp,
    )
