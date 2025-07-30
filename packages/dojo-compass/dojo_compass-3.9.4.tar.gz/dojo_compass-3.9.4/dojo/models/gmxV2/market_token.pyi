from dataclasses import dataclass

@dataclass
class MarketPoolValueInfo:
    pool_value: int
    long_pnl: int
    short_pnl: int
    net_pnl: int
    long_token_amount: int
    short_token_amount: int
    long_token_usd: int
    short_token_usd: int
    total_borrowing_fees: int
    borrowing_fee_pool_factor: int
    impact_pool_amount: int
    def __init__(self, pool_value, long_pnl, short_pnl, net_pnl, long_token_amount, short_token_amount, long_token_usd, short_token_usd, total_borrowing_fees, borrowing_fee_pool_factor, impact_pool_amount) -> None: ...
