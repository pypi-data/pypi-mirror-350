import logging
from collections import OrderedDict

from .models.luis_settings import Rules
from .rule import get_final_intent

logger = logging.getLogger(__name__)


def _format_luis_prediction_response_for_rules(luis_prediction_response: dict) -> dict:
    predicted_intent_name = luis_prediction_response["topIntent"]
    predicted_intent_index = -1
    for i, intent in enumerate(luis_prediction_response["intents"]):
        if intent["category"] == predicted_intent_name:
            predicted_intent_index = i
    prediction_for_rules_computation = {
        "intent_0": {
            "name": predicted_intent_name,
            "confidence": luis_prediction_response["intents"][predicted_intent_index][
                "confidenceScore"
            ]
            * 100,
        },
        "entities": [],
    }

    for entity in luis_prediction_response["entities"]:
        entity_value = entity["text"]

        if entity.get("extraInformation") and entity["extraInformation"][0][
            "extraInformationKind"
        ] in ["ListKey", "RegexKey"]:
            entity_value = entity["extraInformation"][0]["key"]

        prediction_for_rules_computation["entities"].append(
            {
                "name": entity["category"],
                "value": entity_value,
                "confidence": entity["confidenceScore"] * 100,
            }
        )

    return prediction_for_rules_computation


def format_prediction_response(
    prediction_response_json: dict, rules: list[Rules], confidence_threshold: float
) -> OrderedDict:
    """Standardizes the prediction response from NLU engine

    Args:
        prediction_response_json (dict): Prediction json from NLU engine
    """

    logger.info("Formatting prediction response: %s", prediction_response_json)

    output_prediction_response_json = OrderedDict(prediction_response_json)

    prediction_response_from_nlu_engine = output_prediction_response_json.pop(
        "prediction"
    )

    predictions_for_rules_computation = _format_luis_prediction_response_for_rules(
        luis_prediction_response=prediction_response_from_nlu_engine
    )

    final_intent = get_final_intent(
        query=output_prediction_response_json["query"],
        predictions=predictions_for_rules_computation,
        rules=rules,
        prediction_confidence_threshold=confidence_threshold,
    )

    output_prediction_response_json["intent"] = final_intent
    output_prediction_response_json["entities"] = predictions_for_rules_computation[
        "entities"
    ]

    output_prediction_response_json["engine"] = "luis"

    output_prediction_response_json[
        "nlu_response"
    ] = prediction_response_from_nlu_engine

    logger.info("Final prediction response: %s", output_prediction_response_json)

    return output_prediction_response_json
