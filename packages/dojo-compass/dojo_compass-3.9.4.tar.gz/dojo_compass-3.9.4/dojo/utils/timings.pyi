from _typeshed import Incomplete
from typing import Callable, ParamSpec, TextIO, TypeVar

class _TimingState:
    class SingleFunction:
        fn_name: Incomplete
        headers: Incomplete
        timings_file_calls: Incomplete
        timings_file_transacts: Incomplete
        def __init__(self, fn_name: str, headers: list[str]) -> None: ...
        def add_timing(self, s: str, result: str, duration: float) -> None: ...
        def write_timings_to_disk(self, file: TextIO) -> None: ...
    functions: Incomplete
    def __init__(self) -> None: ...
    def register_function(self, sf: SingleFunction) -> None: ...

state: Incomplete
Args = ParamSpec('Args')
Return = TypeVar('Return')

def time_function(*, headers: list[str], args_to_log_string: Callable[Args, str]) -> Callable[[Callable[Args, Return]], Callable[Args, Return]]: ...
