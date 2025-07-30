"""Model for GMX V2 position."""

from dataclasses import dataclass
from decimal import Decimal

from dataclasses_json import LetterCase, dataclass_json
from eth_abi.abi import encode
from eth_utils.crypto import keccak
from hexbytes import HexBytes

ORACLE_DECIMALS = 30
ORACLE_SCALING_FACTOR = 10**ORACLE_DECIMALS


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Addresses:
    """Addresses of a position in GMX V2."""

    account: str
    market: str
    collateral_token: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Numbers:
    """Numbers of a position in GMX V2."""

    size_in_usd: int
    size_in_tokens: int
    collateral_amount: int
    borrowing_factor: int
    funding_fee_amount_per_size: int
    long_token_claimable_funding_amount_per_size: int
    short_token_claimable_funding_amount_per_size: int
    increased_at_block: int
    decreased_at_block: int
    increased_at_time: int
    decreased_at_time: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Flags:
    """Flags of a position in GMX V2."""

    is_long: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Position:
    """Position representation in GMX V2."""

    addresses: Addresses
    numbers: Numbers
    flags: Flags

    @classmethod
    def from_data(
        cls, data: list[tuple[tuple[str], tuple[int], tuple[bool]]]
    ) -> list["Position"]:
        """Create a list of Position objects from raw data.

        :param data: A list of tuples, where each tuple contains:
            - A tuple of strings representing the addresses.
            - A tuple of integers representing the numerical values.
            - A tuple of booleans representing the flags.
        :return: A list of Position objects.
        """
        return [cls(Addresses(*d[0]), Numbers(*d[1]), Flags(*d[2])) for d in data]  # type: ignore

    @property
    def key(self) -> HexBytes:
        """Generate a unique key for the position.

        This key is derived from the account address, market address, collateral token
        address, and the position's long/short flag. It is used to uniquely identify a
        position in the GMX V2 system.

        :return: A HexBytes object representing the unique key for the position.
        """
        _key = keccak(
            encode(
                ["address", "address", "address", "bool"],
                [
                    self.addresses.account,
                    self.addresses.market,
                    self.addresses.collateral_token,
                    self.flags.is_long,
                ],
            )
        )
        return HexBytes(_key)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PositionPnl:
    """Position PnL representation in GMX V2."""

    position_pnl_usd: Decimal
    uncapped_position_pnl_usd: Decimal
    size_delta_in_tokens: Decimal

    def __post_init__(self) -> None:
        """Make sure all values are in USD."""
        self.position_pnl_usd = Decimal(self.position_pnl_usd) / Decimal(
            ORACLE_SCALING_FACTOR
        )
        self.uncapped_position_pnl_usd = Decimal(
            self.uncapped_position_pnl_usd
        ) / Decimal(ORACLE_SCALING_FACTOR)
        self.size_delta_in_tokens = Decimal(self.size_delta_in_tokens) / Decimal(
            ORACLE_SCALING_FACTOR
        )
