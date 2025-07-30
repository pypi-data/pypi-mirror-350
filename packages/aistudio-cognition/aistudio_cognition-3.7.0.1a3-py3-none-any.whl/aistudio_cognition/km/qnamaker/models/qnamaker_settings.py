from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class QnAMakerPredictionSettings:
    no_of_results: int = 1
    threshold: float = 0.5
    short_answers: bool = False
    short_answer_threshold: float = 0.5


@dataclass_json
@dataclass
class QnAMaker:
    prediction_settings: QnAMakerPredictionSettings
    endpoint: str
    ocp_apim_key: str
