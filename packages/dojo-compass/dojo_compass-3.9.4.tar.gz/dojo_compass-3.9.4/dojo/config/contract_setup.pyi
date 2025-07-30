from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from eth_typing import HexAddress as HexAddress, HexStr as HexStr

@dataclass
class SetCode(DataClassJsonMixin):
    code: bytes
    def __init__(self, *generated_args, code, **generated_kwargs) -> None: ...

@dataclass
class SetStorage(DataClassJsonMixin):
    slot_address: HexAddress
    slot_value: HexStr
    def __init__(self, *generated_args, slot_address, slot_value, **generated_kwargs) -> None: ...

@dataclass
class CreateContract(DataClassJsonMixin):
    abi: str
    address: HexAddress
    block_number: int
    transaction_index: int
    set_code: SetCode
    set_storages: list[SetStorage]
    def save(self, path: str) -> None: ...
    @staticmethod
    def load(path: str) -> CreateContract: ...
    def __init__(self, *generated_args, abi, address, block_number, transaction_index, set_code, set_storages, **generated_kwargs) -> None: ...
