import json
import logging
from copy import deepcopy
from typing import Union

import requests
from aistudio_cognition.km.genai.models.genai_settings import GenAI
from aistudio_cognition.models.response_status import ResponseStatus

logger = logging.getLogger(__name__)


class AIStudioKMGenAI:
    def __init__(
        self,
        km_details: Union[dict, GenAI],
        project_name: str = "",
        connection_name: str = "",
    ) -> None:
        if isinstance(km_details, dict):
            self.km_genai = GenAI.from_dict(km_details)
        elif isinstance(km_details, GenAI):
            self.km_genai = km_details
        else:
            raise TypeError(
                "Method argument km_details should either be a dictionary or a GenAI object!"
            )

        self.project_name = project_name
        self.connection_name = connection_name
        response = self._validate_genai_details()
        if not response["success"]:
            error_message = ""
            if self.connection_name:
                error_message = f"Connection : {self.connection_name}, "
            error_message += (
                f"Project : {self.project_name}, Error : {response['message']}"
            )
            raise ValueError(error_message)

    def _validate_genai_details(self) -> ResponseStatus:
        if not self.km_genai.url:
            return ResponseStatus(
                success=False,
                message="KM Service not configured for this project version",
            )
        if not self.km_genai.km_project_id:
            return ResponseStatus(
                success=False,
                message="KM Project ID not configured for this project version",
            )
        if not self.km_genai.km_project_secret:
            return ResponseStatus(
                success=False,
                message="KM Project Secret not configured for this project version",
            )
        return ResponseStatus(success=True)

    def authenticate(self) -> ResponseStatus:
        headers = {
            "Project-Id": self.km_genai.km_project_id,
            "Project-Secret": self.km_genai.km_project_secret,
        }
        try:
            response = requests.get(f"{self.km_genai.url}/api/token", headers=headers)
        except requests.exceptions.ConnectionError as exc:
            logger.exception(f"Failed to establish a connection with KM service, {exc}")
            return ResponseStatus(
                success=False,
                message="Failed to establish a connection with KM service",
            )

        if response.status_code != 200:
            logger.exception(
                f"Error while authenticating with KM Service {self.km_genai.url}, {response.status_code}, {response.text}."
            )
            try:
                response_json = response.json()
                return ResponseStatus(
                    success=False,
                    message=f"Error while authenticating with KM Service, {response_json.get('message', 'Unknown error')}.",
                )
            except json.JSONDecodeError:
                return ResponseStatus(
                    success=False,
                    message=f"Error while authenticating with KM Service {self.km_genai.url}, {response.status_code}, {response.text}.",
                )
        try:
            token = response.json().get("token")
        except requests.exceptions.JSONDecodeError as e:
            logger.exception(f"Could not parse KM service authentication response, {e}")
            return ResponseStatus(
                success=False,
                message="Could not parse KM service authentication response",
            )

        return ResponseStatus(success=True, data=token)

    def _get_payload(
        self,
        query: str,
        history: list = None,
        filters: list = None,
        debug: bool = False,
        **kwargs,
    ):
        payload = {}

        # Add history with latest user query
        history_copy = deepcopy(history)
        if history_copy:
            history_copy.append({"user": query})
        else:
            history_copy = [{"user": query}]
        payload["history"] = history_copy

        # Add filters
        if filters:
            payload["filters"] = filters

        # Add prediction settings
        payload["overrides"] = {
            "retrieval_mode": "vectors",
        }

        payload["debug"] = debug
        # Add the kwargs as well
        # payload = {**kwargs}

        return payload

    def genai_query(
        self,
        token: str,
        query: str,
        history: list = None,
        filters: list = None,
        debug: bool = False,
        **kwargs,
    ):
        headers = {"Authorization": f"Bearer {token}"}
        try:
            payload = self._get_payload(query, history, filters, debug, **kwargs)
            url = f"{self.km_genai.url}/api/query"

            logger.info("Send request to KM Service url: %s", url)
            logger.info("Payload: %s", payload)

            km_response = requests.post(url, headers=headers, data=json.dumps(payload))
            logger.info("Response Status Code: %s", km_response.status_code)

            try:
                response = json.loads(km_response.text)
            except json.JSONDecodeError as exc:
                logger.exception(exc)
                raise Exception("Improper response received from KM Service.")
            if "error" in response and "message" in response.get("error"):
                raise Exception(response.get("error").get("message"))
            return response
        except ConnectionError as exc:
            logger.exception(exc)
            raise Exception("Unable to establish a connection with the KM Service.")

    async def genai_query_streaming(
        self,
        token: str,
        query: str,
        history: list = None,
        filters: list = None,
        debug: bool = False,
        **kwargs,
    ):
        headers = {"Authorization": f"Bearer {token}"}
        try:
            payload = self._get_payload(query, history, filters, debug, **kwargs)
            url = f"{self.km_genai.url}/api/query/stream"

            logger.info("Send request to KM Service url: %s", url)
            logger.info("with headers: %s", headers)
            logger.info("Payload: %s", payload)

            import httpx

            # httpx is not added as a dependency to aistudio-cognition right now
            # This method is used only by chatbot-webservice, which already has httpx dependency
            # Did not want httpx dependency to be added in aistudio for now (to prevent potential conflicts)
            async with httpx.AsyncClient(timeout=300) as client:
                async with client.stream(
                    method="POST",
                    url=url,
                    data=json.dumps(payload),
                    headers=headers,
                ) as km_response:
                    async for text in km_response.aiter_text():
                        yield text
            logger.info("Response Status Code: %s", km_response.status_code)
        except ConnectionError as exc:
            logger.exception(exc)
            raise Exception("Unable to establish a connection with the KM Service.")
