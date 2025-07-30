import base64
import logging
import operator
import re
from typing import TypedDict

from aistudio_cognition.nlu.models import Category

from .models.luis_settings import Rules

logger = logging.getLogger(__name__)


class RuleReturnDict(TypedDict):
    name: str
    confidence: int


def entity_matches_rule(entity_rule: dict, predicted_entity: dict) -> bool:
    """Function to check if entity_rule matches predicted_entity

    Args:
        entity_rule (Dict): Entity rule to be checked
        predicted_entity (Dict): Predicted entity from delta

    Returns:
        bool: True if match is found else False
    """
    return (
        entity_rule["name"] == predicted_entity["name"]
        and entity_rule["value"] in [predicted_entity["value"], ""]
        and entity_rule["confidence"] <= predicted_entity["confidence"]
    )


def evaluate_entity_rule(entity_rules: dict, predicted_entities: dict) -> bool:
    """Evaluate entity rule with AND and OR conditions

    Args:
    entity_rules: json with entity rules
                  Keys: operation: (AND/OR)
                        group: json containing entities/other operations to be
                               evaluated
    predicted_entities: json with predicted entities
    """
    if "group" not in entity_rules:
        return any(
            entity_matches_rule(entity_rules, predicted_entity)
            for predicted_entity in predicted_entities
        )
    entity_matches = []
    for entity_rule in entity_rules["group"]:
        # if item is another expression, evaluate
        if "operation" in entity_rule:
            entity_matches.append(evaluate_entity_rule(entity_rule, predicted_entities))
        else:
            entity_match = any(
                entity_matches_rule(entity_rule, predicted_entity)
                for predicted_entity in predicted_entities
            )
            entity_matches.append(entity_match)

    if entity_rules["operation"].upper() == "AND":
        return all(entity_matches)
    elif entity_rules["operation"].upper() == "OR":
        return any(entity_matches)


def evaluate_intent_rule(category_rules: list[Category], predictions: dict) -> bool:
    intent_matches = []  # list of bools - True if predicted intent satisfies rule

    for category_rule in category_rules:
        category_level = category_rule.level
        intent_match = any(
            (
                intent_rule.name == predictions[f"intent_{category_level}"]["name"]
                and float(intent_rule.confidence)
                <= predictions[f"intent_{category_level}"]["confidence"]
            )
            for intent_rule in category_rule.intents
        )
        intent_matches.append(intent_match)

    # intent condition satisfied if all category rules are met
    return all(intent_matches)


def evaluate_regex_rule(regex_rule: str, query: str) -> bool:
    pattern = base64.b64decode(regex_rule).decode("utf-8")
    return bool(re.search(pattern, query))


def get_final_intent(
    query: str,
    predictions: dict,
    rules: list[Rules],
    prediction_confidence_threshold: float,
    default_prediction_category_level: int = 0,
) -> RuleReturnDict:
    """Function to get final intent from given rules

    Args:
        query (str): Input query/sentence
        predictions (dict): Delta predictions
        rules (Rules): Rules model object
        default_prediction_category_level (int): The intent from this category
            level is set to final intent in case none match

    Returns:
        str: Final intent for the given predictions
    """
    logger.debug("Evaluating final intent for query: %s", query)

    rules.sort(key=operator.attrgetter("priority"))

    for rule in rules:
        intent_condition = False
        entity_condition = False
        regex_condition = False

        if not rule.categories:
            intent_condition = True

        else:
            intent_condition = evaluate_intent_rule(rule.categories, predictions)

        if not rule.entities:
            entity_condition = (
                True  # ignore checking for entities if not present in rule
            )
        else:
            entity_condition = evaluate_entity_rule(
                rule.entities, predictions["entities"]
            )

        if not rule.regex:
            regex_condition = True
        else:
            regex_condition = evaluate_regex_rule(rule.regex, query)
        # return leaf intent if intent, entity and regex rules are satisfied
        if intent_condition and entity_condition and regex_condition:
            return {"name": rule.name, "confidence": 100}

    # in case no rule matches,

    # if intent from default category level is present with confidence higher
    # than default confidence threshold, return that
    if (
        predictions[f"intent_{default_prediction_category_level}"].get("confidence")
        is not None
    ) and (
        prediction_confidence_threshold
        <= predictions[f"intent_{default_prediction_category_level}"]["confidence"]
    ):
        return predictions[f"intent_{default_prediction_category_level}"]

    # else, return intent None
    return {"name": "None", "confidence": 0}
