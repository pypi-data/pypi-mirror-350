from _typeshed import Incomplete
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class LimitOrderOperator(Enum):
    LTE = 0
    GTE = 1

@dataclass
class LimitOrderDefinition:
    trigger_price: Decimal
    key: str
    order_id: int
    operator: LimitOrderOperator
    def __lt__(self, other: LimitOrderDefinition) -> bool: ...
    def __init__(self, trigger_price, key, order_id, operator) -> None: ...

class LimitOrderDefinitionHeap:
    heap: Incomplete
    def __init__(self) -> None: ...
    def push(self, limit_order_definition: LimitOrderDefinition) -> None: ...
    def pop(self) -> LimitOrderDefinition: ...
    def peek(self) -> LimitOrderDefinition: ...
    def __len__(self) -> int: ...
