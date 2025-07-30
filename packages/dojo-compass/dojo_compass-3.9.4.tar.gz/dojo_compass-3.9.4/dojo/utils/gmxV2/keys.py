"""These functions replicate https://github.com/gmx-io/gmx-synthetics/blob/main/contracts/data/Keys.sol."""

from typing import Union

from eth_abi.abi import encode
from eth_utils.crypto import keccak


def generate_key(value: str, *args: Union[str, bool, int]) -> bytes:
    """Utility function to generate keys."""
    return keccak(encode(["string"] * (1 + len(args)), [value, *args]))


WNT = generate_key("WNT")
NONCE = generate_key("NONCE")
FEE_RECEIVER = generate_key("FEE_RECEIVER")
HOLDING_ADDRESS = generate_key("HOLDING_ADDRESS")
MIN_HANDLE_EXECUTION_ERROR_GAS = generate_key("MIN_HANDLE_EXECUTION_ERROR_GAS")
MIN_HANDLE_EXECUTION_ERROR_GAS_TO_FORWARD = generate_key(
    "MIN_HANDLE_EXECUTION_ERROR_GAS_TO_FORWARD"
)
MIN_ADDITIONAL_GAS_FOR_EXECUTION = generate_key("MIN_ADDITIONAL_GAS_FOR_EXECUTION")
REENTRANCY_GUARD_STATUS = generate_key("REENTRANCY_GUARD_STATUS")
DEPOSIT_FEE_TYPE = generate_key("DEPOSIT_FEE_TYPE")
WITHDRAWAL_FEE_TYPE = generate_key("WITHDRAWAL_FEE_TYPE")
SWAP_FEE_TYPE = generate_key("SWAP_FEE_TYPE")
POSITION_FEE_TYPE = generate_key("POSITION_FEE_TYPE")
UI_DEPOSIT_FEE_TYPE = generate_key("UI_DEPOSIT_FEE_TYPE")
UI_WITHDRAWAL_FEE_TYPE = generate_key("UI_WITHDRAWAL_FEE_TYPE")
UI_SWAP_FEE_TYPE = generate_key("UI_SWAP_FEE_TYPE")
UI_POSITION_FEE_TYPE = generate_key("UI_POSITION_FEE_TYPE")
UI_FEE_FACTOR = generate_key("UI_FEE_FACTOR")
MAX_UI_FEE_FACTOR = generate_key("MAX_UI_FEE_FACTOR")
CLAIMABLE_FEE_AMOUNT = generate_key("CLAIMABLE_FEE_AMOUNT")
CLAIMABLE_UI_FEE_AMOUNT = generate_key("CLAIMABLE_UI_FEE_AMOUNT")
MAX_AUTO_CANCEL_ORDERS = generate_key("MAX_AUTO_CANCEL_ORDERS")
MAX_TOTAL_CALLBACK_GAS_LIMIT_FOR_AUTO_CANCEL_ORDERS = generate_key(
    "MAX_TOTAL_CALLBACK_GAS_LIMIT_FOR_AUTO_CANCEL_ORDERS"
)
MARKET_LIST = generate_key("MARKET_LIST")
FEE_BATCH_LIST = generate_key("FEE_BATCH_LIST")
DEPOSIT_LIST = generate_key("DEPOSIT_LIST")
ACCOUNT_DEPOSIT_LIST = generate_key("ACCOUNT_DEPOSIT_LIST")
WITHDRAWAL_LIST = generate_key("WITHDRAWAL_LIST")
ACCOUNT_WITHDRAWAL_LIST = generate_key("ACCOUNT_WITHDRAWAL_LIST")
SHIFT_LIST = generate_key("SHIFT_LIST")
ACCOUNT_SHIFT_LIST = generate_key("ACCOUNT_SHIFT_LIST")
GLV_LIST = generate_key("GLV_LIST")
GLV_DEPOSIT_LIST = generate_key("GLV_DEPOSIT_LIST")
ACCOUNT_GLV_DEPOSIT_LIST = generate_key("ACCOUNT_GLV_DEPOSIT_LIST")
GLV_SUPPORTED_MARKET_LIST = generate_key("GLV_SUPPORTED_MARKET_LIST")
POSITION_LIST = generate_key("POSITION_LIST")
ACCOUNT_POSITION_LIST = generate_key("ACCOUNT_POSITION_LIST")
ORDER_LIST = generate_key("ORDER_LIST")
ACCOUNT_ORDER_LIST = generate_key("ACCOUNT_ORDER_LIST")
SUBACCOUNT_LIST = generate_key("SUBACCOUNT_LIST")
AUTO_CANCEL_ORDER_LIST = generate_key("AUTO_CANCEL_ORDER_LIST")
IS_MARKET_DISABLED = generate_key("IS_MARKET_DISABLED")
MAX_SWAP_PATH_LENGTH = generate_key("MAX_SWAP_PATH_LENGTH")
SWAP_PATH_MARKET_FLAG = generate_key("SWAP_PATH_MARKET_FLAG")
MIN_MARKET_TOKENS_FOR_FIRST_DEPOSIT = generate_key(
    "MIN_MARKET_TOKENS_FOR_FIRST_DEPOSIT"
)
CREATE_GLV_DEPOSIT_FEATURE_DISABLED = generate_key(
    "CREATE_GLV_DEPOSIT_FEATURE_DISABLED"
)
CANCEL_GLV_DEPOSIT_FEATURE_DISABLED = generate_key(
    "CANCEL_GLV_DEPOSIT_FEATURE_DISABLED"
)
EXECUTE_GLV_DEPOSIT_FEATURE_DISABLED = generate_key(
    "EXECUTE_GLV_DEPOSIT_FEATURE_DISABLED"
)
GLV_SHIFT_FEATURE_DISABLED = generate_key("GLV_SHIFT_FEATURE_DISABLED")
CREATE_DEPOSIT_FEATURE_DISABLED = generate_key("CREATE_DEPOSIT_FEATURE_DISABLED")
CANCEL_DEPOSIT_FEATURE_DISABLED = generate_key("CANCEL_DEPOSIT_FEATURE_DISABLED")
EXECUTE_DEPOSIT_FEATURE_DISABLED = generate_key("EXECUTE_DEPOSIT_FEATURE_DISABLED")
CREATE_WITHDRAWAL_FEATURE_DISABLED = generate_key("CREATE_WITHDRAWAL_FEATURE_DISABLED")
CANCEL_WITHDRAWAL_FEATURE_DISABLED = generate_key("CANCEL_WITHDRAWAL_FEATURE_DISABLED")
EXECUTE_WITHDRAWAL_FEATURE_DISABLED = generate_key(
    "EXECUTE_WITHDRAWAL_FEATURE_DISABLED"
)
EXECUTE_ATOMIC_WITHDRAWAL_FEATURE_DISABLED = generate_key(
    "EXECUTE_ATOMIC_WITHDRAWAL_FEATURE_DISABLED"
)
CREATE_SHIFT_FEATURE_DISABLED = generate_key("CREATE_SHIFT_FEATURE_DISABLED")
CANCEL_SHIFT_FEATURE_DISABLED = generate_key("CANCEL_SHIFT_FEATURE_DISABLED")
EXECUTE_SHIFT_FEATURE_DISABLED = generate_key("EXECUTE_SHIFT_FEATURE_DISABLED")
CREATE_ORDER_FEATURE_DISABLED = generate_key("CREATE_ORDER_FEATURE_DISABLED")
EXECUTE_ORDER_FEATURE_DISABLED = generate_key("EXECUTE_ORDER_FEATURE_DISABLED")
EXECUTE_ADL_FEATURE_DISABLED = generate_key("EXECUTE_ADL_FEATURE_DISABLED")
UPDATE_ORDER_FEATURE_DISABLED = generate_key("UPDATE_ORDER_FEATURE_DISABLED")
CANCEL_ORDER_FEATURE_DISABLED = generate_key("CANCEL_ORDER_FEATURE_DISABLED")
CLAIM_FUNDING_FEES_FEATURE_DISABLED = generate_key(
    "CLAIM_FUNDING_FEES_FEATURE_DISABLED"
)
CLAIM_COLLATERAL_FEATURE_DISABLED = generate_key("CLAIM_COLLATERAL_FEATURE_DISABLED")
CLAIM_AFFILIATE_REWARDS_FEATURE_DISABLED = generate_key(
    "CLAIM_AFFILIATE_REWARDS_FEATURE_DISABLED"
)
CLAIM_UI_FEES_FEATURE_DISABLED = generate_key("CLAIM_UI_FEES_FEATURE_DISABLED")
SUBACCOUNT_FEATURE_DISABLED = generate_key("SUBACCOUNT_FEATURE_DISABLED")
MIN_ORACLE_SIGNERS = generate_key("MIN_ORACLE_SIGNERS")
MIN_ORACLE_BLOCK_CONFIRMATIONS = generate_key("MIN_ORACLE_BLOCK_CONFIRMATIONS")
MAX_ORACLE_PRICE_AGE = generate_key("MAX_ORACLE_PRICE_AGE")
MAX_ORACLE_TIMESTAMP_RANGE = generate_key("MAX_ORACLE_TIMESTAMP_RANGE")
MAX_ORACLE_REF_PRICE_DEVIATION_FACTOR = generate_key(
    "MAX_ORACLE_REF_PRICE_DEVIATION_FACTOR"
)
IS_ORACLE_PROVIDER_ENABLED = generate_key("IS_ORACLE_PROVIDER_ENABLED")
IS_ATOMIC_ORACLE_PROVIDER = generate_key("IS_ATOMIC_ORACLE_PROVIDER")
ORACLE_TIMESTAMP_ADJUSTMENT = generate_key("ORACLE_TIMESTAMP_ADJUSTMENT")
ORACLE_PROVIDER_FOR_TOKEN = generate_key("ORACLE_PROVIDER_FOR_TOKEN")
CHAINLINK_PAYMENT_TOKEN = generate_key("CHAINLINK_PAYMENT_TOKEN")
SEQUENCER_GRACE_DURATION = generate_key("SEQUENCER_GRACE_DURATION")
POSITION_FEE_RECEIVER_FACTOR = generate_key("POSITION_FEE_RECEIVER_FACTOR")
SWAP_FEE_RECEIVER_FACTOR = generate_key("SWAP_FEE_RECEIVER_FACTOR")
BORROWING_FEE_RECEIVER_FACTOR = generate_key("BORROWING_FEE_RECEIVER_FACTOR")
ESTIMATED_GAS_FEE_BASE_AMOUNT_V2_1 = generate_key("ESTIMATED_GAS_FEE_BASE_AMOUNT_V2_1")
ESTIMATED_GAS_FEE_PER_ORACLE_PRICE = generate_key("ESTIMATED_GAS_FEE_PER_ORACLE_PRICE")
ESTIMATED_GAS_FEE_MULTIPLIER_FACTOR = generate_key(
    "ESTIMATED_GAS_FEE_MULTIPLIER_FACTOR"
)
EXECUTION_GAS_FEE_BASE_AMOUNT_V2_1 = generate_key("EXECUTION_GAS_FEE_BASE_AMOUNT_V2_1")
EXECUTION_GAS_FEE_PER_ORACLE_PRICE = generate_key("EXECUTION_GAS_FEE_PER_ORACLE_PRICE")
EXECUTION_GAS_FEE_MULTIPLIER_FACTOR = generate_key(
    "EXECUTION_GAS_FEE_MULTIPLIER_FACTOR"
)
DEPOSIT_GAS_LIMIT = generate_key("DEPOSIT_GAS_LIMIT")
WITHDRAWAL_GAS_LIMIT = generate_key("WITHDRAWAL_GAS_LIMIT")
GLV_DEPOSIT_GAS_LIMIT = generate_key("GLV_DEPOSIT_GAS_LIMIT")
GLV_PER_MARKET_GAS_LIMIT = generate_key("GLV_PER_MARKET_GAS_LIMIT")
SHIFT_GAS_LIMIT = generate_key("SHIFT_GAS_LIMIT")
SINGLE_SWAP_GAS_LIMIT = generate_key("SINGLE_SWAP_GAS_LIMIT")
INCREASE_ORDER_GAS_LIMIT = generate_key("INCREASE_ORDER_GAS_LIMIT")
DECREASE_ORDER_GAS_LIMIT = generate_key("DECREASE_ORDER_GAS_LIMIT")
SWAP_ORDER_GAS_LIMIT = generate_key("SWAP_ORDER_GAS_LIMIT")
TOKEN_TRANSFER_GAS_LIMIT = generate_key("TOKEN_TRANSFER_GAS_LIMIT")
NATIVE_TOKEN_TRANSFER_GAS_LIMIT = generate_key("NATIVE_TOKEN_TRANSFER_GAS_LIMIT")
REQUEST_EXPIRATION_TIME = generate_key("REQUEST_EXPIRATION_TIME")
MAX_CALLBACK_GAS_LIMIT = generate_key("MAX_CALLBACK_GAS_LIMIT")
REFUND_EXECUTION_FEE_GAS_LIMIT = generate_key("REFUND_EXECUTION_FEE_GAS_LIMIT")
SAVED_CALLBACK_CONTRACT = generate_key("SAVED_CALLBACK_CONTRACT")
MIN_COLLATERAL_FACTOR = generate_key("MIN_COLLATERAL_FACTOR")
MIN_COLLATERAL_FACTOR_FOR_OPEN_INTEREST_MULTIPLIER = generate_key(
    "MIN_COLLATERAL_FACTOR_FOR_OPEN_INTEREST_MULTIPLIER"
)
MIN_COLLATERAL_USD = generate_key("MIN_COLLATERAL_USD")
MIN_POSITION_SIZE_USD = generate_key("MIN_POSITION_SIZE_USD")
VIRTUAL_TOKEN_ID = generate_key("VIRTUAL_TOKEN_ID")
VIRTUAL_MARKET_ID = generate_key("VIRTUAL_MARKET_ID")
VIRTUAL_INVENTORY_FOR_SWAPS = generate_key("VIRTUAL_INVENTORY_FOR_SWAPS")
VIRTUAL_INVENTORY_FOR_POSITIONS = generate_key("VIRTUAL_INVENTORY_FOR_POSITIONS")
POSITION_IMPACT_FACTOR = generate_key("POSITION_IMPACT_FACTOR")
POSITION_IMPACT_EXPONENT_FACTOR = generate_key("POSITION_IMPACT_EXPONENT_FACTOR")
MAX_POSITION_IMPACT_FACTOR = generate_key("MAX_POSITION_IMPACT_FACTOR")
MAX_POSITION_IMPACT_FACTOR_FOR_LIQUIDATIONS = generate_key(
    "MAX_POSITION_IMPACT_FACTOR_FOR_LIQUIDATIONS"
)
MAX_PNL_FACTOR_FOR_TRADERS = generate_key("MAX_PNL_FACTOR_FOR_TRADERS")
MAX_PNL_FACTOR_FOR_DEPOSITS = generate_key("MAX_PNL_FACTOR_FOR_DEPOSITS")
MAX_PNL_FACTOR_FOR_WITHDRAWALS = generate_key("MAX_PNL_FACTOR_FOR_WITHDRAWALS")


def account_key(prefix: bytes, account: str) -> bytes:
    """Utility function to generate keys."""
    return keccak(encode(["bytes32", "address"], [prefix, account]))


# def account_market_key(prefix: bytes, account: str, market: str) -> bytes:
#     """Utility function to generate keys."""
#     return keccak(encode(["bytes32", "address", "address"], [prefix, account, market]))


# def account_token_key(prefix: bytes, account: str, token: str) -> bytes:
#     """Utility function to generate keys."""
#     return keccak(encode(["bytes32", "address", "address"], [prefix, account, token]))


# def market_key(prefix: bytes, market: str) -> bytes:
#     """Utility function to generate keys."""
#     return keccak(encode(["bytes32", "address"], [prefix, market]))


# def market_bool_key(prefix: bytes, market: str, is_long: bool) -> bytes:
#     """Utility function to generate keys."""
#     return keccak(encode(["bytes32", "address", "bool"], [prefix, market, is_long]))


# def account_deposit_list_key(account: str) -> bytes:
#     """Utility function to generate keys."""
#     return account_key(ACCOUNT_DEPOSIT_LIST, account)


# def account_withdrawal_list_key(account: str) -> bytes:
#     """Utility function to generate keys."""
#     return account_key(ACCOUNT_WITHDRAWAL_LIST, account)


# def account_shift_list_key(account: str) -> bytes:
#     """Utility function to generate keys."""
#     return account_key(ACCOUNT_SHIFT_LIST, account)


# def account_glv_deposit_list_key(account: str) -> bytes:
#     """Utility function to generate keys."""
#     return account_key(ACCOUNT_GLV_DEPOSIT_LIST, account)


# def glv_supported_market_list_key(glv: str) -> bytes:
#     """Utility function to generate keys."""
#     return account_key(GLV_SUPPORTED_MARKET_LIST, glv)


# def account_position_list_key(account: str) -> bytes:
#     """Utility function to generate keys."""
#     return account_key(ACCOUNT_POSITION_LIST, account)


# def account_order_list_key(account: str) -> bytes:
#     """Utility function to generate keys."""
#     return account_key(ACCOUNT_ORDER_LIST, account)


# def subaccount_list_key(account: str) -> bytes:
#     """Utility function to generate keys."""
#     return account_key(SUBACCOUNT_LIST, account)


# def auto_cancel_order_list_key(position_key: bytes) -> bytes:
#     """Utility function to generate keys."""
#     return keccak(
#         encode(["bytes32", "bytes32"], [AUTO_CANCEL_ORDER_LIST, position_key])
#     )


# def claimable_fee_amount_key(market: str, token: str) -> bytes:
#     """Utility function to generate keys."""
#     return account_token_key(CLAIMABLE_FEE_AMOUNT, market, token)


# def claimable_ui_fee_amount_key(
#     market: str, token: str, account: Optional[str] = None
# ) -> bytes:
#     """Utility function to generate keys."""
#     if account:
#         return account_token_key(CLAIMABLE_UI_FEE_AMOUNT, market, token, account)
#     return account_token_key(CLAIMABLE_UI_FEE_AMOUNT, market, token)


# def deposit_gas_limit_key(single_token: bool) -> bytes:
#     """Utility function to generate keys."""
#     return keccak(encode(["bytes32", "bool"], [DEPOSIT_GAS_LIMIT, single_token]))


def token_transfer_gas_limit(token: str) -> bytes:
    """Get account key for `TOKEN_TRANSFER_GAS_LIMIT`."""
    return account_key(TOKEN_TRANSFER_GAS_LIMIT, token)
