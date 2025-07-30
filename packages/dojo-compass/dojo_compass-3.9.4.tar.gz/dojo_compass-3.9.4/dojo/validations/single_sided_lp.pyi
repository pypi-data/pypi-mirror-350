from decimal import Decimal
from dojo.observations.uniswapV3 import UniswapV3Observation as UniswapV3Observation

def validate_single_sided_lp(quote: tuple[Decimal, Decimal], tick_range: tuple[int, int], pool: str, obs: UniswapV3Observation) -> None: ...
