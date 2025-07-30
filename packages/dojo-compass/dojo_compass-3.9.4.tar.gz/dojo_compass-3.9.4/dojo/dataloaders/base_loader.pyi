import abc
from _typeshed import Incomplete
from abc import ABC
from dojo.common.constants import Chain as Chain
from dojo.common.time_to_block import time_to_block as time_to_block
from dojo.config import cfg as cfg
from typing import Any

QUERY_FOR_DATA_INGESTED_BY_DOJO: Incomplete

def address_to_name(chain: Chain, protocol: str, address: str) -> str: ...

class BaseLoader(ABC, metaclass=abc.ABCMeta):
    def __init__(self, **kwargs: Any) -> None: ...
