"""Utility functions to perform actions similar to TokenUtils library."""
from typing import Any

from web3.contract.contract import Contract
from web3.types import PendingTx

from dojo.network.base_backend import BaseBackend
from dojo.utils.gmxV2.keys import REQUEST_EXPIRATION_TIME


def set_uint(
    backend: BaseBackend,
    contract: Contract,
    function_params: tuple[bytes | int],
) -> PendingTx:
    """Set uint on Datastore contract."""
    return backend.contract_transact(
        contract.functions.setUint, function_params=function_params
    )


def get_uint(backend: BaseBackend, contract: Contract, key: bytes) -> Any:
    """Get uint from Datastore contract."""
    return backend.contract_call(contract.functions.getUint, [key])


def get_request_expiration_time(
    backend: BaseBackend,
    contract: Contract,
) -> Any:
    """Get request expiration time from Datastore contract."""
    return get_uint(backend, contract, REQUEST_EXPIRATION_TIME)
