import json
import logging
from json import JSONDecodeError
from typing import Union

import requests
from requests.exceptions import ConnectionError

from aistudio_cognition.models.response_status import ResponseStatus

from .models.qnamaker_settings import QnAMaker

logger = logging.getLogger(__name__)


class AIStudioKMQnAMaker:
    def __init__(
        self,
        km_details: Union[dict, QnAMaker],
        project_name: str = "",
        connection_name: str = "",
    ) -> None:
        if isinstance(km_details, dict):
            self.km_qnamaker = QnAMaker.from_dict(km_details)
        elif isinstance(km_details, QnAMaker):
            self.km_qnamaker = km_details
        else:
            raise TypeError(
                "Method argument km_details should either be a dictionary or a QnAMaker "
                "object!"
            )
        self.project_name = project_name
        self.connection_name = connection_name
        response = self._validate_qnamaker_details()
        if not response["success"]:
            error_message = ""
            if self.connection_name:
                error_message = f"Connection : {self.connection_name}, "
            error_message += (
                f"Project : {self.project_name}, Error : {response['message']}"
            )
            raise ValueError(error_message)

    def _validate_qnamaker_details(self) -> ResponseStatus:
        if not self.km_qnamaker.prediction_settings:
            return ResponseStatus(
                success=False,
                message="KM prediction settings not configured for this project version",
            )
        if not self.km_qnamaker.endpoint:
            return ResponseStatus(
                success=False,
                message="KM prediction URL not configured for this project version",
            )

        return ResponseStatus(success=True)

    def qnamaker_query(
        self,
        query: str,
        qnaId: int,
        context: dict,
    ) -> ResponseStatus:
        payload = {"question": query}

        payload["confidenceScoreThreshold"] = (
            self.km_qnamaker.prediction_settings.threshold
        )
        payload["top"] = self.km_qnamaker.prediction_settings.no_of_results
        if qnaId:
            payload["qnaId"] = qnaId
        if context:
            payload["context"] = context
            payload["filters"] = {
                "metadataFilter": {"metadata": [], "logicalOperation": "AND"}
            }
        if self.km_qnamaker.prediction_settings.short_answers:
            payload["answerSpanRequest"] = {
                "enable": self.km_qnamaker.prediction_settings.short_answers,
                "confidenceScoreThreshold": self.km_qnamaker.prediction_settings.short_answer_threshold,
            }
        headers = {
            "ocp-apim-subscription-key": self.km_qnamaker.ocp_apim_key,
            "Content-Type": "application/json",
        }
        try:
            logger.info("Send request to QnA Maker url: %s", self.km_qnamaker.endpoint)
            logger.info("with headers: %s", headers)
            logger.info("Payload: %s", payload)
            km_response = requests.post(
                self.km_qnamaker.endpoint, headers=headers, data=json.dumps(payload)
            )
            logger.info("Response received from QnA Maker: %s", km_response.text)
            logger.info("Response Status Code: %s", km_response.status_code)
        except ConnectionError as exc:
            logger.exception(exc)
            return ResponseStatus(
                success=False,
                message="Unable to establish a connection with the QnA Maker Service.",
            )
        try:
            response = json.loads(km_response.text)
        except JSONDecodeError as exc:
            logger.exception(exc)
            return ResponseStatus(
                success=False,
                message="Improper response received. "
                + "Please check if the Hostname and Knowledgebase Id are rightly configured.",
            )
        if "error" in response and "message" in response.get("error"):
            return ResponseStatus(
                success=False, message=response.get("error").get("message")
            )
        if response.get("answers") and km_response.status_code == 200:
            if (
                len(response.get("answers")) == 1
                and len(response.get("answers")[0].get("questions")) == 0
            ):
                response = {"result": [], "engine": "QnAMAKER"}
            else:
                response = {
                    "result": list(
                        map(
                            lambda answer: {
                                "id": answer.get("id"),
                                "details": answer.get("answer"),
                                "title": (
                                    answer.get("questions")[0]
                                    if answer.get("questions")
                                    else ""
                                ),
                                "score": answer.get("confidenceScore"),
                                "dialog": answer.get("dialog", {}),
                                "answerSpan": (
                                    answer.get("answerSpan")
                                    if answer.get("answerSpan")
                                    else {}
                                ),
                            },
                            response.get("answers"),
                        )
                    ),
                    "engine": "QnAMAKER",
                }
            return ResponseStatus(success=True, data=response)
        else:
            return ResponseStatus(
                success=False, message="Unable to get a proper response from QnAMaker."
            )
