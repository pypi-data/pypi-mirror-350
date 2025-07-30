from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from aistudio_cognition.nlu.models import Rules


@dataclass_json
@dataclass
class LUISSettings:
    authoring_url: str
    subscription_key: str
    project_name: str
    deployment_name: str
    api_version: str


@dataclass_json
@dataclass
class LUIS:
    rules: list[Rules]
    confidence_threshold: float
    luis_settings: Optional[LUISSettings] = None
