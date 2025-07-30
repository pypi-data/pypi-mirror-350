"""Adapter functions to transform user actions to dojo internal actions."""

from dojo.actions.gmxV2.deposit.models import GmxDeposit, GmxLPDeposit
from dojo.actions.gmxV2.deposit.params import (
    CreateDepositParams,
    CreateDepositParamsAddresses,
    CreateDepositParamsNumbers,
)
from dojo.actions.gmxV2.orders.base_models import GmxOrder
from dojo.actions.gmxV2.orders.models import (
    GmxBaseTraderOrder,
    GmxDecreaseLongLimitOrder,
    GmxDecreaseLongMarketOrder,
    GmxDecreaseShortLimitOrder,
    GmxDecreaseShortMarketOrder,
    GmxIncreaseLongLimitOrder,
    GmxIncreaseLongMarketOrder,
    GmxIncreaseShortLimitOrder,
    GmxIncreaseShortMarketOrder,
    GmxSwapOrder,
    OrderDef,
)
from dojo.actions.gmxV2.orders.params import DecreasePositionSwapType, OrderType
from dojo.actions.gmxV2.utils import (
    _calculate_execution_fee,
    _get_acceptable_price,
    _get_estimated_swap_output,
    _get_initial_collateral_delta_amount,
    _get_long_token_amount,
    _get_short_token_amount,
    _get_swap_path,
)
from dojo.actions.gmxV2.withdrawal.models import GmxLPWithdrawal, GmxWithdrawal
from dojo.config.deployments import get_address, get_decimals
from dojo.models.gmxV2.market import _get_gmx_market_address_to_market, _get_gmx_markets
from dojo.money.format import to_human_format, to_machine_format
from dojo.network.constants import GMX_ORACLE_PRECISION, ZERO_ADDRESS


def deposit_adapter(lp_deposit: GmxDeposit, deposit_id: int) -> GmxLPDeposit:
    """Function to convert user submitted deposit to a GMX deposit."""
    initial_long_token_address = lp_deposit.observations.backend.contracts[
        lp_deposit.initial_long_token_symbol
    ].address
    initial_short_token_address = lp_deposit.observations.backend.contracts[
        lp_deposit.initial_short_token_symbol
    ].address

    market = lp_deposit.observations.get_market(lp_deposit.market_key)
    long_token_amount_in_collateral = _get_long_token_amount(
        lp_deposit.long_token_usd,
        lp_deposit.observations,
        lp_deposit.initial_long_token_symbol,
    )
    short_token_amount_in_collateral = _get_short_token_amount(
        lp_deposit.short_token_usd,
        lp_deposit.observations,
        lp_deposit.initial_short_token_symbol,
    )
    long_token_amount_for_market_token_calculation = _get_long_token_amount(
        lp_deposit.long_token_usd, lp_deposit.observations, market.long_token.symbol
    )
    short_token_amount_for_market_token_calculation = _get_short_token_amount(
        lp_deposit.short_token_usd, lp_deposit.observations, market.short_token.symbol
    )
    long_decimals = get_decimals(
        lp_deposit.observations.chain, lp_deposit.initial_long_token_symbol
    )
    short_decimals = get_decimals(
        lp_deposit.observations.chain, lp_deposit.initial_short_token_symbol
    )

    scaled_long_token_amount = to_machine_format(
        long_token_amount_in_collateral, long_decimals
    )
    scaled_short_token_amount = to_machine_format(
        short_token_amount_in_collateral, short_decimals
    )

    long_decimals_for_market_token_calculation = market.long_token.decimals
    short_decimals_for_market_token_calculation = market.short_token.decimals
    scaled_long_token_amount_for_market_token_calculation = to_machine_format(
        long_token_amount_for_market_token_calculation,
        long_decimals_for_market_token_calculation,
    )
    scaled_short_token_amount_for_market_token_calculation = to_machine_format(
        short_token_amount_for_market_token_calculation,
        short_decimals_for_market_token_calculation,
    )

    if lp_deposit.initial_long_token_symbol != market.long_token.symbol:
        long_token_swap_path, _ = _get_swap_path(
            lp_deposit.agent,
            lp_deposit.initial_long_token_symbol,
            market.long_token.symbol,
        )
    else:
        long_token_swap_path = []

    if lp_deposit.initial_short_token_symbol != market.short_token.symbol:
        short_token_swap_path, _ = _get_swap_path(
            lp_deposit.agent,
            lp_deposit.initial_short_token_symbol,
            market.short_token.symbol,
        )
    else:
        short_token_swap_path = []

    execution_fee = _calculate_execution_fee(lp_deposit.agent, deposit=True)

    min_market_tokens = lp_deposit.observations.get_deposit_amount_out(
        lp_deposit.market_key,
        int(scaled_long_token_amount_for_market_token_calculation),
        int(scaled_short_token_amount_for_market_token_calculation),
        False,
    )
    create_deposit_params = CreateDepositParams(
        addresses=CreateDepositParamsAddresses(
            receiver=lp_deposit.agent.original_address,
            market=market.market_token.address,
            initial_long_token=initial_long_token_address,
            initial_short_token=initial_short_token_address,
            long_token_swap_path=long_token_swap_path,
            short_token_swap_path=short_token_swap_path,
        ),
        numbers=CreateDepositParamsNumbers(
            initial_long_token_amount=int(scaled_long_token_amount),
            initial_short_token_amount=int(scaled_short_token_amount),
            min_market_tokens=0,
            execution_fee=execution_fee,
            callback_gas_limit=0,
        ),
        should_unwrap_native_token=False,
    )
    return GmxLPDeposit(
        agent=lp_deposit.agent,
        create_deposit_params=create_deposit_params,
        deposit_id=deposit_id,
        initial_long_token_symbol=lp_deposit.initial_long_token_symbol,
        initial_short_token_symbol=lp_deposit.initial_short_token_symbol,
        long_token_amount=long_token_amount_in_collateral,
        short_token_amount=short_token_amount_in_collateral,
        gm_token_amount=to_human_format(
            min_market_tokens, market.market_token.decimals
        ),
        market_key=lp_deposit.market_key,
    )


def order_adapter(user_order: GmxBaseTraderOrder, order_id: int) -> GmxOrder:
    """Function to adapt the order to the correct type."""
    action_to_order_type = {
        GmxIncreaseLongMarketOrder: OrderDef(
            order_type=OrderType.MARKET_INCREASE, is_long=True, is_limit_order=False
        ),
        GmxDecreaseLongMarketOrder: OrderDef(
            order_type=OrderType.MARKET_DECREASE, is_long=True, is_limit_order=False
        ),
        GmxIncreaseShortMarketOrder: OrderDef(
            order_type=OrderType.MARKET_INCREASE, is_long=False, is_limit_order=False
        ),
        GmxDecreaseShortMarketOrder: OrderDef(
            order_type=OrderType.MARKET_DECREASE, is_long=False, is_limit_order=False
        ),
        GmxIncreaseLongLimitOrder: OrderDef(
            order_type=OrderType.LIMIT_INCREASE, is_long=True, is_limit_order=True
        ),
        GmxDecreaseLongLimitOrder: OrderDef(
            order_type=OrderType.LIMIT_DECREASE, is_long=True, is_limit_order=True
        ),
        GmxIncreaseShortLimitOrder: OrderDef(
            order_type=OrderType.LIMIT_INCREASE, is_long=False, is_limit_order=True
        ),
        GmxDecreaseShortLimitOrder: OrderDef(
            order_type=OrderType.LIMIT_DECREASE, is_long=False, is_limit_order=True
        ),
    }

    order_definition = action_to_order_type[type(user_order)]
    order_type = order_definition.order_type
    is_long = order_definition.is_long
    is_limit_order = order_definition.is_limit_order

    market_key_to_market = _get_gmx_markets(chain=user_order.agent.backend.chain)
    market = market_key_to_market[user_order.market_key]

    swap_path: list[str] = []
    token_in_symbol: str = user_order.token_in_symbol
    if order_type in {OrderType.MARKET_DECREASE, OrderType.LIMIT_DECREASE}:
        # if the order is a decrease order, the token_in_symbol is the collateral token
        # as the position key is decided by the collateral token
        token_in_symbol = user_order.collateral_token_symbol

    if token_in_symbol != user_order.collateral_token_symbol:
        swap_path, _ = _get_swap_path(
            user_order.agent, token_in_symbol, user_order.collateral_token_symbol
        )

    execution_fee = _calculate_execution_fee(user_order.agent, order_type)

    collateral_address = get_address(
        user_order.observations.chain, "Tokens", token_in_symbol
    )
    collateral_decimals = get_decimals(user_order.observations.chain, token_in_symbol)

    addresses = {
        "receiver": user_order.agent.original_address,
        "account": user_order.agent.original_address,
        "initial_collateral_token": collateral_address,
        "market": market.market_token.address,
        "swap_path": swap_path,
    }

    initial_collateral_delta_amount = _get_initial_collateral_delta_amount(
        size_delta_usd=user_order.size_delta_usd,
        leverage=user_order.leverage,
        collateral_token_symbol=token_in_symbol,
        observations=user_order.observations,
    )
    acceptable_price = _get_acceptable_price(
        market_key=user_order.market_key,
        order_type=order_type,
        is_long=is_long,
        slippage=user_order.slippage,
        observations=user_order.observations,
    )
    trigger_price = (
        user_order.trigger_price  # type: ignore
        if is_limit_order
        else user_order.observations.index_token_price(user_order.market_key)
    )

    numbers = {
        "size_delta_usd": to_machine_format(
            user_order.size_delta_usd, GMX_ORACLE_PRECISION
        ),
        "initial_collateral_delta_amount": to_machine_format(
            initial_collateral_delta_amount, collateral_decimals
        ),
        "trigger_price": to_machine_format(
            trigger_price, GMX_ORACLE_PRECISION - market.index_token.decimals
        ),
        "acceptable_price": to_machine_format(
            acceptable_price, GMX_ORACLE_PRECISION - market.index_token.decimals
        ),
        "execution_fee": execution_fee,
        "callback_gas_limit": 0,
        "min_output_amount": 0,
    }
    create_order_params = {
        "addresses": addresses,
        "numbers": numbers,
        "order_type": order_type,
        "decrease_position_swap_type": DecreasePositionSwapType.NO_SWAP,
        "is_long": is_long,
        "should_unwrap_native_token": False,
        "auto_cancel": False,
    }
    return GmxOrder.from_dict(
        {
            "create_order_params": create_order_params,
            "agent": user_order.agent,
            # protobuf args
            "market_key": user_order.market_key,
            "leverage": user_order.leverage,
            "token_in_symbol": token_in_symbol,
            "collateral_symbol": user_order.collateral_token_symbol,
            "order_id": order_id,
        }
    )


def swap_adapter(swap: GmxSwapOrder, order_id: int) -> GmxOrder:
    """Function to convert user submitted swap order to a GMX swap order."""
    agent = swap.agent

    in_token = swap.in_token
    out_token = swap.out_token
    initial_collateral_delta = swap.in_token_amount
    slippage = swap.slippage

    decimal = get_decimals(agent.backend.chain, in_token)
    initial_collateral_delta_amount = to_machine_format(
        initial_collateral_delta, decimal
    )

    swap_path, _ = _get_swap_path(agent, in_token, out_token)

    estimated_output_amount, price_impact_usd = _get_estimated_swap_output(
        agent,
        _get_gmx_market_address_to_market(agent.backend.chain)[
            agent.backend.address2name[swap_path[0]].replace("GM:", "")  # type: ignore #TODO(lukas) fix
        ],
        swap.observations,
        in_token,
        initial_collateral_delta_amount,
    )
    if len(swap_path) > 1:
        estimated_output_amount, price_impact_usd = _get_estimated_swap_output(
            agent,
            _get_gmx_market_address_to_market(agent.backend.chain)[
                agent.backend.address2name[swap_path[1]].replace("GM:", "")  # type: ignore #TODO(lukas) fix
            ],
            swap.observations,
            "USDC",
            int(estimated_output_amount - estimated_output_amount * slippage / 10000),
        )

    min_output_amount = int(
        estimated_output_amount - estimated_output_amount * slippage / 10000
    )

    execution_fee = _calculate_execution_fee(agent, OrderType.MARKET_SWAP)

    addresses = {
        "receiver": agent.original_address,
        "account": agent.original_address,
        "initial_collateral_token": agent.backend.name2address[in_token],
        "market": ZERO_ADDRESS,
        "swap_path": swap_path,
    }
    numbers = {
        "size_delta_usd": 0,
        "initial_collateral_delta_amount": initial_collateral_delta_amount,
        "trigger_price": 0,
        "acceptable_price": 0,
        "execution_fee": execution_fee,
        "callback_gas_limit": 0,
        "min_output_amount": min_output_amount,
    }
    create_order_params = {
        "addresses": addresses,
        "numbers": numbers,
        "order_type": OrderType.MARKET_SWAP,
        "decrease_position_swap_type": DecreasePositionSwapType.NO_SWAP,
        "is_long": False,
        "should_unwrap_native_token": True,
    }
    return GmxOrder.from_dict(
        {
            "create_order_params": create_order_params,
            "agent": agent,
            "out_token": out_token,
            "market_key": ZERO_ADDRESS,
            "leverage": 1,
            "token_in_symbol": in_token,
            "collateral_symbol": in_token,
            "order_id": order_id,
            "observations": swap.observations,
        }
    )


def withdrawal_adapter(
    withdrawal: GmxWithdrawal, withdrawal_id: int
) -> GmxLPWithdrawal:
    """Function to convert user submitted withdrawal to a GMX withdrawal."""
    agent = withdrawal.agent
    market_key = withdrawal.market_key
    gm_token_amount = withdrawal.gm_token_amount

    market_key_to_market = _get_gmx_markets(chain=agent.backend.chain)
    market = market_key_to_market[market_key]
    execution_fee = _calculate_execution_fee(agent, withdraw=True)

    create_withdrawal_params = {
        "receiver": agent.original_address,
        "callback_contract": agent.original_address,
        "market": market.market_token.address,
        "long_token_swap_path": [],
        "short_token_swap_path": [],
        "min_long_token_amount": 0,
        "min_short_token_amount": 0,
        "market_token_amount": to_machine_format(gm_token_amount, 18),
        "execution_fee": execution_fee,
        "callback_gas_limit": 0,
        "should_unwrap_native_token": False,
        "ui_fee_receiver": ZERO_ADDRESS,
    }
    return GmxLPWithdrawal.from_dict(
        {
            "create_withdrawal_params": create_withdrawal_params,
            "agent": agent,
            "withdrawal_id": withdrawal_id,
            "market_key": market_key,
            "gm_token_amount": gm_token_amount,
        }
    )
