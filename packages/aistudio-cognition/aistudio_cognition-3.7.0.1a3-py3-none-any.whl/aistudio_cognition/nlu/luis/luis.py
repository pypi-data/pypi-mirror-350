import json
import logging
from time import sleep
from typing import Union

import requests
from requests.exceptions import ConnectionError, HTTPError

from aistudio_cognition.models.response_status import ResponseStatus

from .models.luis_settings import LUIS
from .prediction import format_prediction_response

logger = logging.getLogger(__name__)


class AIStudioNLULUIS:
    def __init__(
        self,
        nlu_details: Union[dict, LUIS],
        project_name: str = "",
        connection_name: str = "",
    ):
        if isinstance(nlu_details, dict):
            self.nlu_luis = LUIS.from_dict(nlu_details)
        elif isinstance(nlu_details, LUIS):
            self.nlu_luis = nlu_details
        else:
            raise TypeError(
                "Method argument nlu_details should either be a dictionary or a LUIS "
                "object!"
            )
        self.project_name = project_name
        self.connection_name = connection_name
        response = self._validate_luis_details()
        if not response["success"]:
            error_message = ""
            if self.connection_name:
                error_message = f"Connection : {self.connection_name}, "
            error_message += (
                f"Project : {self.project_name}, Error : {response['message']}"
            )
            raise ValueError(error_message)

    def _validate_luis_details(self) -> ResponseStatus:
        if not self.nlu_luis.luis_settings:
            return ResponseStatus(
                success=False,
                message="LUIS settings not configured for this project version",
            )
        if not self.nlu_luis.luis_settings.authoring_url:
            return ResponseStatus(
                success=False,
                message="LUIS prediction URL not configured for this project version",
            )

        return ResponseStatus(success=True)

    def fetch_objects_using_settings(self) -> ResponseStatus:
        export_url = (
            f"{self.nlu_luis.luis_settings.authoring_url}/language/authoring/"
            "analyze-conversations/projects/"
            f"{self.nlu_luis.luis_settings.project_name}/:export?stringIndexType="
            "Utf16CodeUnit"
            f"&api-version={self.nlu_luis.luis_settings.api_version}"
        )

        headers = {
            "Ocp-Apim-Subscription-Key": self.nlu_luis.luis_settings.subscription_key
        }
        try:
            logger.debug("Sending Export Call to CLU")
            export_response = requests.post(export_url, headers=headers)
        except Exception as e:
            logger.exception(e)
            return ResponseStatus(
                success=False,
                message=(
                    "Connection Failed! Please verify if the Authoring URL, Project "
                    + "Name and API Version are rightly configured"
                ),
            )
        if export_response.status_code in {401, 403, 429}:
            response_json = export_response.json()
            logger.error(response_json.get("error"))
            return ResponseStatus(
                success=False,
                message=response_json.get("error", {}).get(
                    "message", "Something went wrong!"
                ),
            )

        operation_location = export_response.headers.get("operation-location")
        result_url = None
        while True:
            logger.debug("Status Request Send")
            try:
                operation_response = requests.get(operation_location, headers=headers)
                operation_data = operation_response.json()
            except Exception as e:
                logger.exception(e)
                return ResponseStatus(success=False, message="Connection Failed!")

            operation_status = operation_data.get("status")
            if operation_status == "succeeded":
                result_url = operation_data.get("resultUrl")
                break
            sleep(1)
        logger.debug("Fetching Intents, Entities and Utterances")
        try:
            response = requests.get(result_url, headers=headers)
            response_data = response.json()
        except Exception as e:
            logger.exception(e)
            return ResponseStatus(success=False, message="Connection Failed!")
        assets = response_data.get("assets")
        intents = assets.get("intents")
        entities = assets.get("entities")
        for intent in intents:
            intent["name"] = intent["category"]
            del intent["category"]
        for entity in entities:
            entity["name"] = entity["category"]
            del entity["category"]

        return ResponseStatus(
            success=True, data={"intents": intents, "entities": entities}
        )

    def make_prediction_call(self, query: str) -> requests.Response:
        conversationItemId = "user__1234"
        participantId = "user__1234"
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.nlu_luis.luis_settings.subscription_key,
        }
        payload = {
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "id": conversationItemId,
                    "text": query,
                    "modality": "text",
                    # "language": "en-us",
                    "participantId": participantId,
                }
            },
            "parameters": {
                "projectName": self.nlu_luis.luis_settings.project_name,
                "deploymentName": self.nlu_luis.luis_settings.deployment_name,
            },
        }
        prediction_url = (
            f"{self.nlu_luis.luis_settings.authoring_url}/language/:analyze-conversations?"
            + f"api-version={self.nlu_luis.luis_settings.api_version}"
        )
        response = requests.post(
            prediction_url, data=json.dumps(payload), headers=headers
        )
        logger.debug(
            "Prediction response from CLU: %s, %s", response.text, response.status_code
        )
        logger.debug("Headers: %s", response.headers)
        response.raise_for_status()
        return response

    def get_predictions(self, query: str) -> ResponseStatus:
        try:
            response = self.make_prediction_call(query)
        except ConnectionError as exc:
            logger.exception(exc)
            return ResponseStatus(
                success=False,
                message="Unable to establish connection to LUIS.",
            )
        except HTTPError as exc:
            logger.exception(exc)
            return ResponseStatus(
                success=False,
                message="Unable to get proper response from LUIS.",
            )

        result = json.loads(response.text)
        luis_prediction_response = format_prediction_response(
            result["result"], self.nlu_luis.rules, self.nlu_luis.confidence_threshold
        )

        return ResponseStatus(success=True, data=luis_prediction_response)
