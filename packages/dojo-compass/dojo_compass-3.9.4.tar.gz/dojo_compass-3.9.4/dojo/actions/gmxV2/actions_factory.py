"""Set of functions to create actions from event data."""
from collections import defaultdict
from typing import Any

from dojo.actions.gmxV2.base_gmx_action import InternalBaseGmxAction as BaseGmxAction
from dojo.actions.gmxV2.deposit.models import GmxHistoricDeposit
from dojo.actions.gmxV2.keeper_actions.models import (
    GmxHistoricExecuteDeposit,
    GmxHistoricExecuteOrder,
    GmxHistoricExecuteWithdrawal,
    SetPricesParams,
)
from dojo.actions.gmxV2.orders.base_models import (
    GmxHistoricOrder,
    GmxHistoricOrderCancel,
    GmxHistoricOrderUpdate,
)
from dojo.actions.gmxV2.orders.params import DecreasePositionSwapType, OrderType
from dojo.actions.gmxV2.withdrawal.models import GmxHistoricWithdrawal
from dojo.agents.base_agent import BaseAgent
from dojo.observations import GmxV2Observation

DEFAULT_PROVIDER = "0x83cBb05AA78014305194450c4AADAc887fe5DF7F"


def _get_addresses(raw_addresses: list[dict[str, Any]]) -> dict[str, str]:
    addresses = {}
    for item in raw_addresses:
        key, value = item.values()
        addresses[key] = value
    return addresses


def _get_address_lists(raw_addresses: list[dict[str, Any]]) -> dict[str, list[str]]:
    addresses = {}
    for item in raw_addresses:
        key, value = item.values()
        addresses[key] = value
    return addresses


def _get_bools(raw_bools: list[dict[str, Any]]) -> dict[str, bool]:
    return {item["key"]: item["value"] for item in raw_bools}


def _get_numbers(
    raw_numbers: list[dict[str, Any]],
) -> tuple[dict[Any, Any], OrderType | None, DecreasePositionSwapType | None]:
    numbers = {}
    order_type = None
    decrease_position_swap_type = None

    for item in raw_numbers:
        if item["key"] == "orderType":
            order_type = OrderType(item["value"])
        elif item["key"] == "decreasePositionSwapType":
            decrease_position_swap_type = DecreasePositionSwapType(item["value"])
        else:
            numbers[item["key"]] = item["value"]
    return numbers, order_type, decrease_position_swap_type


def _get_bytes(raw_bytes: list[dict[str, Any]]) -> dict[str, str]:
    return {item["key"]: item["value"] for item in raw_bytes}


def _create_market_order(
    event_data: dict[str, Any], agent: BaseAgent[GmxV2Observation]
) -> tuple[GmxHistoricOrder, Any]:
    """Class method to instantiate an CreateOrder object from event data."""
    addresses = _get_addresses(event_data["addressItems"]["items"])
    (
        numbers,
        order_type,
        decrease_position_swap_type,
    ) = _get_numbers(event_data["uintItems"]["items"])
    bools = _get_bools(event_data["boolItems"]["items"])
    original_key = event_data["bytes32Items"]["items"][0]["value"]
    return (
        GmxHistoricOrder.from_dict(
            {
                "create_order_params": {
                    "addresses": addresses,
                    "numbers": numbers,
                    "order_type": order_type,
                    "decrease_position_swap_type": decrease_position_swap_type,
                    **bools,
                },
                "agent": agent,
                "original_key": original_key,
            }
        ),
        original_key,
    )


def _create_market_deposit(
    event_data: dict[str, Any], agent: BaseAgent[GmxV2Observation]
) -> tuple[GmxHistoricDeposit, None]:
    """Class method to instantiate an GmxHistoricDeposit object from event data."""
    addresses = _get_addresses(event_data["addressItems"]["items"])
    (numbers, _, _) = _get_numbers(event_data["uintItems"]["items"])
    bools = _get_bools(event_data["boolItems"]["items"])
    original_key = event_data["bytes32Items"]["items"][0]["value"]
    return (
        GmxHistoricDeposit.from_dict(
            {
                "create_deposit_params": {
                    "addresses": addresses,
                    "numbers": numbers,
                    **bools,
                },
                "agent": agent,
                "original_key": original_key,
            }
        ),
        original_key,
    )


def _create_order_executed(
    event_data: dict[str, Any], agent: BaseAgent[GmxV2Observation], block: int
) -> tuple[GmxHistoricExecuteOrder, Any]:
    """Class method to instantiate an GmxExecuteOrder object from event data."""
    bytes_ = _get_bytes(event_data["bytes32Items"]["items"])

    return (
        GmxHistoricExecuteOrder(agent=agent, key=bytes_["key"], block=block),
        None,
    )


def _create_deposit_executed(
    event_data: dict[str, Any], agent: BaseAgent[GmxV2Observation], block: int
) -> tuple[GmxHistoricExecuteDeposit, Any]:
    """Class method to instantiate an GmxExecuteDeposit object from event data."""
    bytes_ = _get_bytes(event_data["bytes32Items"]["items"])

    return (
        GmxHistoricExecuteDeposit(agent=agent, key=bytes_["key"], block=block),
        None,
    )


def _create_withdrawal_executed(
    event_data: dict[str, Any], agent: BaseAgent[GmxV2Observation], block: int
) -> tuple[GmxHistoricExecuteWithdrawal, Any]:
    """Class method to instantiate an GmxExecuteWithdrawal object from event data."""
    bytes_ = _get_bytes(event_data["bytes32Items"]["items"])

    return (
        GmxHistoricExecuteWithdrawal(agent=agent, key=bytes_["key"], block=block),
        None,
    )


def _cancel_market_order(
    event_data: dict[str, Any], agent: BaseAgent[GmxV2Observation]
) -> tuple[GmxHistoricOrderCancel, Any]:
    """Class method to instantiate an GmxCancelOrder object from event data."""
    addresses = _get_addresses(event_data["addressItems"]["items"])  # account
    bytes_items = _get_bytes(event_data["bytesItems"]["items"])  # reasonBytes
    string_items = _get_bytes(event_data["stringItems"]["items"])  # reason
    original_key = event_data["bytes32Items"]["items"][0]["value"]
    return (
        GmxHistoricOrderCancel(
            agent=agent,
            account=addresses["account"],
            key=original_key,
            reasonBytes=bytes_items["reasonBytes"],
            reason=string_items["reason"],
        ),
        original_key,
    )


def _create_market_withdrawal(
    event_data: dict[str, Any], agent: BaseAgent[GmxV2Observation]
) -> tuple[GmxHistoricWithdrawal, Any]:
    """Class method to instantiate an GmxHistoricWithdrawal object from event data."""
    addresses = _get_addresses(event_data["addressItems"]["items"])
    address_lists = _get_address_lists(event_data["addressItems"]["arrayItems"])
    (numbers, _, _) = _get_numbers(event_data["uintItems"]["items"])
    bools = _get_bools(event_data["boolItems"]["items"])
    original_key = event_data["bytes32Items"]["items"][0]["value"]
    return (
        GmxHistoricWithdrawal.from_dict(
            {
                "create_withdrawal_params": {
                    **addresses,
                    **address_lists,
                    **numbers,
                    **bools,
                },
                "agent": agent,
                "original_key": original_key,
            }
        ),
        original_key,
    )


def _update_market_order(
    event_data: dict[str, Any], agent: BaseAgent[GmxV2Observation]
) -> tuple[GmxHistoricOrderUpdate, Any]:
    """Class method to instantiate an GmxUpdateOrder object from event data."""
    addresses = _get_addresses(event_data["addressItems"]["items"])
    (numbers, _, _) = _get_numbers(event_data["uintItems"]["items"])
    bools = _get_bools(event_data["boolItems"]["items"])
    original_key = event_data["bytes32Items"]["items"][0]["value"]
    return (
        GmxHistoricOrderUpdate.from_dict(
            {
                "key": original_key,
                **addresses,
                **numbers,
                **bools,
                "agent": agent,
            }
        ),
        original_key,
    )


def _process_price_oracle_update(
    event_data: dict[str, Any]
) -> tuple[SetPricesParams, str]:
    addresses = _get_addresses(event_data["addressItems"]["items"])
    price_numbers = _get_numbers(event_data["uintItems"]["items"])[0]
    set_prices_params = SetPricesParams(
        tokens=[addresses["token"]],
        providers=[addresses.get("provider", DEFAULT_PROVIDER)],
        data=[price_numbers],
    )
    return set_prices_params, addresses["token"]


def _process_oracle_prices(
    oracle_prices: defaultdict[str, dict[int, SetPricesParams]],
    from_block: int,
    to_block: int,
) -> defaultdict[int, dict[str, SetPricesParams]]:
    intermediate_prices: defaultdict[str, dict[int, SetPricesParams]] = defaultdict(
        dict
    )
    # TODO this piece of code is extremely inefficient, we should refactor it
    # 1) we can get prices for the tokens required only as currently we get prices for all tokens
    # in all GMX markets, the db query does not allow us to filter them as of now
    # 2) the code itself cane be made more efficient
    # 3) we can get the prices for the required tokens only from the oracle
    for token, prices in oracle_prices.items():
        items = sorted([*prices.items()], key=lambda x: x[0])
        for index, (block, price) in enumerate(items):
            if len(prices) == 1:
                for i in range(from_block, to_block + 1):
                    intermediate_prices[token][i] = price
            elif index == 0:
                for i in range(from_block, items[1][0] + 1):
                    intermediate_prices[token][i] = price
            elif index == len(prices) - 1:
                for i in range(block, to_block + 1):
                    intermediate_prices[token][i] = price
            else:
                for i in range(block + 1, items[index + 1][0] + 1):
                    intermediate_prices[token][i] = price

    processed_prices: defaultdict[int, dict[str, SetPricesParams]] = defaultdict(dict)
    for token, prices in intermediate_prices.items():
        for block, price in prices.items():
            processed_prices[block][token] = price

    return processed_prices


def _events_to_actions(
    events: list[dict[str, Any]],
    agent: BaseAgent[GmxV2Observation],
    from_block: int,
    to_block: int,
) -> tuple[
    defaultdict[Any | None, list[BaseGmxAction]],
    dict[Any, BaseGmxAction],
    defaultdict[int, dict[str, SetPricesParams]],
]:
    block_to_actions = defaultdict(list)
    original_key_to_action: dict[str, BaseGmxAction] = {}
    event_name_to_action = {
        "OrderCreated": _create_market_order,
        "DepositCreated": _create_market_deposit,
        "WithdrawalCreated": _create_market_withdrawal,
        "OrderExecuted": _create_order_executed,
        "DepositExecuted": _create_deposit_executed,
        "OrderCancelled": _cancel_market_order,
        "WithdrawalExecuted": _create_withdrawal_executed,
        "OrderUpdated": _update_market_order,
    }
    oracle_prices: defaultdict[str, dict[int, SetPricesParams]] = defaultdict(dict)
    for event in events:
        event_name = event["event_data"]["eventName"]
        block_number = event["block"]
        if event_name == "OraclePriceUpdate":
            set_prices_params, token = _process_price_oracle_update(
                event["event_data"]["eventData"]
            )
            oracle_prices[token][block_number] = set_prices_params
        else:
            factory_method = event_name_to_action.get(event_name)
            kwargs = {"event_data": event["event_data"]["eventData"], "agent": agent}
            if event_name in {
                "OrderExecuted",
                "DepositExecuted",
                "WithdrawalExecuted",
            }:
                kwargs["block"] = block_number
            if factory_method is not None:
                action, original_key = factory_method(**kwargs)  # type: ignore
                block_to_actions[block_number].append(action)
                if original_key:
                    original_key_to_action[original_key] = action

    processed_oracle_prices = _process_oracle_prices(
        oracle_prices, from_block, to_block
    )

    return block_to_actions, original_key_to_action, processed_oracle_prices
