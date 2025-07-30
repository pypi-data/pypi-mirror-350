from _typeshed import Incomplete
from dojo.config import cfg as cfg
from typing import Any

gmx_abis: Incomplete
aave_abis: Incomplete

def debug_gmx_error(error_args: tuple[Any, ...]) -> tuple[str, str]: ...
def debug_aave_error(error_code: Any) -> str: ...
