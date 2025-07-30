from enum import Enum

class StrEnum(str, Enum): ...

class Chain(StrEnum):
    ARBITRUM = 'arbitrum'
    ETHEREUM = 'ethereum'
    GNOSIS = 'gnosis'
