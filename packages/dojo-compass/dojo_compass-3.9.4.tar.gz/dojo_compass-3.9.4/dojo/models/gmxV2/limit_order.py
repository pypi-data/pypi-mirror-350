"""Classes used to perform limit order executions."""
import heapq
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class LimitOrderOperator(Enum):
    """This operator enum is used to determine the operator of the limit order."""

    LTE = 0
    GTE = 1


@dataclass
class LimitOrderDefinition:
    """Definition of a node for limit order heap."""

    trigger_price: Decimal
    key: str
    order_id: int
    operator: LimitOrderOperator

    def __lt__(self, other: "LimitOrderDefinition") -> bool:
        """Less than operator."""
        if self.operator is LimitOrderOperator.LTE:
            return self.trigger_price < other.trigger_price
        else:
            return self.trigger_price > other.trigger_price


class LimitOrderDefinitionHeap:
    """This class is used to maintain a min heap of limit order definitions."""

    def __init__(self) -> None:
        """Initialize the min heap."""
        self.heap: list[LimitOrderDefinition] = []

    def push(self, limit_order_definition: LimitOrderDefinition) -> None:
        """Push a limit order definition to the heap."""
        heapq.heappush(self.heap, limit_order_definition)

    def pop(self) -> LimitOrderDefinition:
        """Pop the top element from the heap."""
        return heapq.heappop(self.heap)

    def peek(self) -> LimitOrderDefinition:
        """Peek the top element from the heap."""
        return self.heap[0]

    def __len__(self) -> int:
        """Length of the heap."""
        return len(self.heap)
