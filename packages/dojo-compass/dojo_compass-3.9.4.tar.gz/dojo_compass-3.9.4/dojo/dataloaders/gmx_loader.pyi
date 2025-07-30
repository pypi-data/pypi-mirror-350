from _typeshed import Incomplete
from dojo.common.constants import Chain as Chain
from dojo.dataloaders.base_loader import BaseLoader as BaseLoader
from dojo.dataloaders.exceptions import MissingIngestedData as MissingIngestedData
from dojo.dataloaders.formats import GMXEvent as GMXEvent

logger: Incomplete
GMX_EVENT_EMITTER_CONTRACT_ADDRESS: Incomplete

class GMXLoader(BaseLoader):
    chain: Incomplete
    block_range: Incomplete
    from_block: Incomplete
    to_block: Incomplete
    def __init__(self, chain: Chain, block_range: tuple[int, int]) -> None: ...
