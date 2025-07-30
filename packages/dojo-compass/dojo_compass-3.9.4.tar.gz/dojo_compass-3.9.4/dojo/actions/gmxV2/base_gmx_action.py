"""Base GMX action."""
from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin, LetterCase, dataclass_json

from dojo.actions.base_action import BaseAction
from dojo.observations import GmxV2Observation

BaseGmxAction = BaseAction[GmxV2Observation]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class InternalBaseGmxAction(DataClassJsonMixin, BaseAction[GmxV2Observation]):
    """Base Action for GMX."""

    pass
