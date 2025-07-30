from _typeshed import Incomplete

ACCOUNT_ID: str
LICENSE_VALIDATION_URL: Incomplete
LICENSE_ACTIVATION_URL: Incomplete
APP_NAME: str
NEEDS_ACTIVATION_CODES: Incomplete
DEVELOPMENT_OVERRIDE_SHA256: str
FIDELITY_TRIAL_OVERRIDE_SHA256: str

def machine_fingerprint() -> str: ...
def activate_license(license_key: str, data_id: str) -> None: ...
def is_development_license(license_key: bytes) -> bool: ...
def assert_license_is_valid(license_key: str) -> None: ...
