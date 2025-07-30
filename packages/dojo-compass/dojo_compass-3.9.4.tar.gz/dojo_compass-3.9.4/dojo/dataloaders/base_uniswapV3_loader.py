"""Base class for UniswapV3 data loader."""
from abc import ABC, abstractmethod
from typing import Literal, Optional

from dojo.common.constants import Chain
from dojo.dataloaders.base_loader import BaseLoader
from dojo.dataloaders.formats import UniswapV3Event


class BaseUniswapV3Loader(BaseLoader, ABC):
    """Abstract class for writing your own UniswapV3 dataloader."""

    @abstractmethod
    def _load_data(self, chain: Chain, pool_addresses: list[str], from_block: int, to_block: int, subset: Optional[list[Literal["Burn", "Mint", "Swap"]]] = None) -> list[UniswapV3Event]:  # type: ignore[override]
        """Load data."""
        pass
