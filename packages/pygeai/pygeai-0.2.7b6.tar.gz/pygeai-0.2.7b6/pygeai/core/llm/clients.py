import json
from json import JSONDecodeError

from pygeai import logger
from pygeai.core.base.clients import BaseClient
from pygeai.core.llm.endpoints import GET_PROVIDER_LIST_V2, GET_PROVIDER_DATA_V2, GET_PROVIDER_MODELS_V2, \
    GET_MODEL_DATA_V2


class LlmClient(BaseClient):

    def get_provider_list(self) -> dict:
        logger.debug("Obtaining provider list")
        response = self.api_service.get(endpoint=GET_PROVIDER_LIST_V2)
        try:
            result = response.json()
        except JSONDecodeError as e:
            result = response.text

        return result

    def get_provider_data(self, provider_name: str) -> dict:
        endpoint = GET_PROVIDER_DATA_V2.format(providerName=provider_name)

        logger.debug(f"Obtaining provider data for {provider_name}")

        response = self.api_service.get(endpoint=endpoint)
        try:
            result = response.json()
        except JSONDecodeError as e:
            result = response.text

        return result

    def get_provider_models(self, provider_name: str) -> dict:
        endpoint = GET_PROVIDER_MODELS_V2.format(providerName=provider_name)

        logger.debug(f"Obtaining provider models for {provider_name}")

        response = self.api_service.get(endpoint=endpoint)
        try:
            result = response.json()
        except JSONDecodeError as e:
            result = response.text

        return result

    def get_model_data(
            self,
            provider_name: str,
            model_name: str = None,
            model_id: str = None
    ) -> dict:
        endpoint = GET_MODEL_DATA_V2.format(
            providerName=provider_name,
            modelNameOrId=model_name or model_id
        )

        logger.debug(f"Obtaining model data for {provider_name}/{model_name or model_id}")

        response = self.api_service.get(endpoint=endpoint)
        try:
            result = response.json()
        except JSONDecodeError as e:
            result = response.text

        return result




