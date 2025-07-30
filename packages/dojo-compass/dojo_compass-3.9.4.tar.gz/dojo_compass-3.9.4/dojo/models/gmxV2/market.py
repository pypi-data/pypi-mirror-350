"""Dataclasses representing GMX markets."""
from dataclasses import dataclass, field
from typing import Any, Optional

from dataclasses_json import DataClassJsonMixin

from dojo.common.constants import Chain
from dojo.config.data.gmx_tokens.arbitrum import ARBITRUM_TOKENS
from dojo.config.data.gmx_tokens.avalanche import AVALANCHE_TOKENS
from dojo.config.deployments import get_all_gmx_markets
from dojo.network.constants import ZERO_ADDRESS


@dataclass
class MarketVenue:
    """Market representation in GMX.

    :param long_token: Long token in the market.
    :param short_token: Short token in the market.
    :param index_token: Index token in the market. No index token if swap only.
    :param swap_only: Whether the market is swap only. This will be updated accordingly.
    """

    long_token: str
    short_token: str
    index_token: Optional[str] = None
    swap_only: bool = False

    def __post_init__(self) -> None:
        """Post init method to check if the market is valid.

        :raises ValueError: If the market is invalid.
        """
        if self.index_token is not None and self.swap_only:
            raise ValueError("Swap only markets don't have an index token.")

    def all_tokens(self) -> list[str]:
        """Returns all tokens for a given market."""
        tokens = [self.long_token, self.short_token]
        if self.index_token is not None:
            tokens.insert(0, self.index_token)
        return tokens

    @property
    def market_key(self) -> str:
        """Key of a single market."""
        if_not_swap_only = (
            self.index_token + ":" if self.index_token is not None else ""
        )
        return f"{if_not_swap_only}{self.long_token}:{self.short_token}"


@dataclass
class Token(DataClassJsonMixin):
    """Token representation in GMX.

    :param symbol: Symbol of the token.
    :param address: Address of the token.
    :param decimals: Decimals of the token.
    :param is_synthetic: Whether the token is synthetic. Defaults to False.
    """

    symbol: str
    address: str
    decimals: int
    is_synthetic: bool = False


@dataclass
class Market(DataClassJsonMixin):
    """Market representation in GMX."""

    long_token: Token
    short_token: Token
    market_token: Token
    # there are markets on GMX that are swap only
    # and do not have an index token
    index_token: Token = field(
        default_factory=lambda: Token(
            symbol="ZERO_ADDRESS", address=ZERO_ADDRESS, decimals=0
        )
    )
    swap_only: bool = False

    @property
    def market_key(self) -> str:
        """Key of a single market."""
        if_not_swap_only = self.index_token.symbol + ":" if not self.swap_only else ""
        return f"{if_not_swap_only}{self.long_token.symbol}:{self.short_token.symbol}"


def _process_raw_market_dict(
    chain: Chain, raw_market_dict: dict[str, tuple[str, str, str, str]]
) -> dict[str, Market]:
    market_key_to_market = {}
    index_to_token_name = {
        0: "index_token",
        1: "long_token",
        2: "short_token",
    }
    symbol_to_token_info, address_to_symbol = _get_gmx_tokens(chain)

    for _, raw_market in raw_market_dict.items():
        market_dict = {}
        market_key_list = []
        for i, token_address in enumerate(raw_market[1:]):
            # skipping index 0 here, cause it is a market token
            # and is not listed on gmx api
            if token_address != ZERO_ADDRESS:
                token_symbol = address_to_symbol[token_address]
                market_key_list.append(token_symbol)
                market_dict[index_to_token_name[i]] = symbol_to_token_info[token_symbol]

        market_key = ":".join(market_key_list)
        market_dict["market_token"] = Token(
            symbol=f"GM:{market_key}", address=raw_market[0], decimals=18
        )
        market = Market.from_dict(market_dict)
        market_key_to_market[market_key] = market

    return market_key_to_market


def _get_gmx_tokens(
    chain: Chain,
) -> tuple[dict[Any, Token], dict[Any, Any]]:

    chain_to_token_config = {"arbitrum": ARBITRUM_TOKENS, "avalanche": AVALANCHE_TOKENS}
    token_config = chain_to_token_config[chain]
    tokens = token_config["tokens"]

    symbol_to_token_info = {}
    address_to_symbol = {}
    for raw_token in tokens:
        raw_token["symbol"] = (
            raw_token["symbol"] if raw_token["symbol"] != "ETH" else "WETH"
        )
        token = Token.from_dict(raw_token)

        symbol = raw_token["symbol"]
        symbol_to_token_info[symbol] = token
        address_to_symbol[raw_token["address"]] = symbol

    return symbol_to_token_info, address_to_symbol


def _get_gmx_markets(chain: Chain) -> dict[str, Market]:
    markets = get_all_gmx_markets(chain)
    raw_market_dict = {
        f"{market[1]}:{market[2]}:{market[3]}": market for market in markets
    }
    available_markets = _process_raw_market_dict(chain, raw_market_dict)
    return available_markets


def _get_gmx_market_address_to_market(chain: Chain) -> dict[str, Market]:
    markets = get_all_gmx_markets(chain)
    raw_market_dict = {f"{market[0]}": market for market in markets}
    available_markets = _process_raw_market_dict(chain, raw_market_dict)
    return available_markets


def _get_all_tokens_from_market(market: Market) -> list[Token]:
    return [market.index_token, market.long_token, market.short_token]


def _get_all_tokens_symbol_to_address(market: Market) -> dict[str, str]:
    return {
        token.symbol: token.address for token in _get_all_tokens_from_market(market)
    }
