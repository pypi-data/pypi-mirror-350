"""Keys and utils methods for roles contracts on gmx."""
from typing import Any

from eth_abi.abi import encode
from eth_utils.crypto import keccak
from web3.contract.contract import Contract

from dojo.network.base_backend import BaseBackend


def generate_key(value: str) -> bytes:
    """Utility function to generate keys."""
    return keccak(encode(["string"], [value]))


ROLE_ADMIN = generate_key("ROLE_ADMIN")
TIMELOCK_ADMIN = generate_key("TIMELOCK_ADMIN")
TIMELOCK_MULTISIG = generate_key("TIMELOCK_MULTISIG")
CONFIG_KEEPER = generate_key("CONFIG_KEEPER")
LIMITED_CONFIG_KEEPER = generate_key("LIMITED_CONFIG_KEEPER")
CONTROLLER = generate_key("CONTROLLER")
GOV_TOKEN_CONTROLLER = generate_key("GOV_TOKEN_CONTROLLER")
ROUTER_PLUGIN = generate_key("ROUTER_PLUGIN")
MARKET_KEEPER = generate_key("MARKET_KEEPER")
FEE_KEEPER = generate_key("FEE_KEEPER")
FEE_DISTRIBUTION_KEEPER = generate_key("FEE_DISTRIBUTION_KEEPER")
ORDER_KEEPER = generate_key("ORDER_KEEPER")
FROZEN_ORDER_KEEPER = generate_key("FROZEN_ORDER_KEEPER")
PRICING_KEEPER = generate_key("PRICING_KEEPER")
LIQUIDATION_KEEPER = generate_key("LIQUIDATION_KEEPER")
ADL_KEEPER = generate_key("ADL_KEEPER")


def get_role_members(
    backend: BaseBackend,
    contract: Contract,
    role_key: bytes,
    start: int = 0,
    end: int = 15,
) -> Any:
    """Get members of a particular role."""
    return backend.contract_call(
        contract.functions.getRoleMembers, [role_key, start, end]
    )


def has_role(
    backend: BaseBackend, contract: Contract, account: str, roleKey: bytes
) -> Any:
    """Check if an account has a particular role."""
    return backend.contract_call(contract.functions.hasRole, [account, roleKey])


def grant_role(
    backend: BaseBackend, contract: Contract, account: str, roleKey: bytes, admin: str
) -> None:
    """Grant a role to a given account."""
    backend.contract_transact(
        contract.functions.grantRole, [account, roleKey], {"from": admin}
    )


# [[0x89efEB90827965f3C26C8eb959f73696f0f7183d]
# [0x83ba9c0623b419B0AFf560775F2a7c2940EF49a3]
# [0xC66a7FAe65f8b733F869F59645ef907a53fceadc]
# [0x45e48668F090a3eD1C7961421c60Df4E66f693BD]
# [0xf040aEDf10948c1F69249226e22EB4856471a3AA]
# [0xBdEFDa2188c0B4c8Dc77302e346BfD8a6721fe7D]
# [0x265f3B4580aA1eCDfe6f252042C3f6cB81599461]]
# GMX gnosis safe owners - need four of these.
