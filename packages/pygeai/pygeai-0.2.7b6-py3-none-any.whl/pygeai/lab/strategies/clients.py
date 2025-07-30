from json import JSONDecodeError

from pygeai import logger
from pygeai.core.base.clients import BaseClient
from pygeai.lab.strategies.endpoints import LIST_REASONING_STRATEGIES_V2, CREATE_REASONING_STRATEGY_V2, \
    UPDATE_REASONING_STRATEGY_V2, UPSERT_REASONING_STRATEGY_V2, GET_REASONING_STRATEGY_V2


class ReasoningStrategyClient(BaseClient):

    def list_reasoning_strategies(
            self,
            name: str = "",
            start: str = "0",
            count: str = "100",
            allow_external: bool = True,
            access_scope: str = "public"
    ):
        """
        Retrieves a list of reasoning strategies available in the system, filtered by the specified criteria.

        :param name: str - Name of the reasoning strategy to filter by. Defaults to an empty string (no filtering).
        :param start: str - Starting index for pagination. Defaults to "0".
        :param count: str - Number of reasoning strategies to retrieve. Defaults to "100".
        :param allow_external: bool - Whether to include external reasoning strategies in the list. Defaults to True.
        :param access_scope: str - Access scope of the reasoning strategies, either "public" or "private". Defaults to "public".
        :return: dict or str - JSON response containing the list of reasoning strategies if successful, otherwise the raw response text.
        :raises ValueError: If access_scope is not "public" or "private".
        :raises Exception: If the request fails due to network issues, authentication errors, or server-side problems.
        """
        valid_access_scopes = ["public", "private"]
        if access_scope not in valid_access_scopes:
            raise ValueError("Access scope must be either 'public' or 'private'.")

        endpoint = LIST_REASONING_STRATEGIES_V2
        headers = {"Authorization": self.api_service.token}
        params = {
            "name": name,
            "start": start,
            "count": count,
            "allowExternal": allow_external,
            "accessScope": access_scope,
        }

        logger.debug("Listing reasoning strategies")

        response = self.api_service.get(endpoint=endpoint, headers=headers, params=params)
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result

    def create_reasoning_strategy(
            self,
            project_id: str,
            name: str,
            system_prompt: str,
            access_scope: str = "public",
            strategy_type: str = "addendum",
            localized_descriptions: list = None,
            automatic_publish: bool = False
    ):
        """
        Creates a new reasoning strategy in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param name: str - Name of the reasoning strategy.
        :param system_prompt: str - System prompt for the reasoning strategy.
        :param access_scope: str - Access scope, either 'public' or 'private'. Defaults to 'public'.
        :param strategy_type: str - Type of the strategy, e.g., 'addendum'. Defaults to 'addendum'.
        :param localized_descriptions: list - List of localized description dictionaries with 'language' and 'description'.
        :param automatic_publish: bool - Whether to automatically publish the reasoning strategy after updating. Defaults to False.
        :return: dict or str - JSON response with the created strategy details if successful, otherwise raw text.
        """
        endpoint = CREATE_REASONING_STRATEGY_V2
        if automatic_publish:
            endpoint = f"{endpoint}?automaticPublish=true"

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "strategyDefinition": {
                "name": name,
                "systemPrompt": system_prompt,
                "accessScope": access_scope,
                "type": strategy_type,
                "localizedDescriptions": localized_descriptions or []
            }
        }

        logger.debug(f"Creating reasoning strategy with data: {data}")

        response = self.api_service.post(endpoint=endpoint, headers=headers, data=data)
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result

    def update_reasoning_strategy(
            self,
            project_id: str,
            reasoning_strategy_id: str,
            name: str = None,
            system_prompt: str = None,
            access_scope: str = None,
            strategy_type: str = None,
            localized_descriptions: list = None,
            automatic_publish: bool = False,
            upsert: bool = False
    ):
        """
        Updates an existing reasoning strategy in the specified project or upserts it if specified.

        :param project_id: str - Unique identifier of the project.
        :param reasoning_strategy_id: str - Unique identifier of the reasoning strategy to update.
        :param name: str, optional - Updated name of the reasoning strategy.
        :param system_prompt: str, optional - Updated system prompt for the reasoning strategy.
        :param access_scope: str, optional - Updated access scope, either 'public' or 'private'.
        :param strategy_type: str, optional - Updated type of the strategy, e.g., 'addendum'.
        :param localized_descriptions: list, optional - Updated list of localized description dictionaries.
        :param automatic_publish: bool - Whether to publish the strategy after updating. Defaults to False.
        :param upsert: bool - Whether to insert the strategy if it does not exist (upsert) instead of just updating. Defaults to False.
        :return: dict or str - JSON response with the updated strategy details if successful, otherwise raw text.
        :raises ValueError: If access_scope is not 'public' or 'private', or if type is not 'addendum'.
        """
        if access_scope is not None:
            valid_access_scopes = ["public", "private"]
            if access_scope not in valid_access_scopes:
                raise ValueError("Access scope must be either 'public' or 'private'.")
        if strategy_type is not None:
            valid_types = ["addendum"]
            if strategy_type not in valid_types:
                raise ValueError("Type must be 'addendum'.")

        data = {
            "strategyDefinition": {}
        }
        if name is not None:
            data["strategyDefinition"]["name"] = name
        if system_prompt is not None:
            data["strategyDefinition"]["systemPrompt"] = system_prompt
        if access_scope is not None:
            data["strategyDefinition"]["accessScope"] = access_scope
        if strategy_type is not None:
            data["strategyDefinition"]["type"] = strategy_type
        if localized_descriptions is not None:
            data["strategyDefinition"]["localizedDescriptions"] = localized_descriptions

        logger.debug(f"Updating reasoning strategy with ID {reasoning_strategy_id} with data: {data}")

        endpoint = UPSERT_REASONING_STRATEGY_V2 if upsert else UPDATE_REASONING_STRATEGY_V2
        endpoint = endpoint.format(reasoningStrategyId=reasoning_strategy_id)

        if automatic_publish:
            endpoint = f"{endpoint}?automaticPublish=true"

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = self.api_service.put(
            endpoint=endpoint,
            headers=headers,
            data=data
        )
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result

    def get_reasoning_strategy(
            self,
            project_id: str,
            reasoning_strategy_id: str = None,
            reasoning_strategy_name: str = None
    ):
        """
        Retrieves details of a specific reasoning strategy in the specified project, identified by either its ID or name.

        :param project_id: str - Unique identifier of the project.
        :param reasoning_strategy_id: str, optional - Unique identifier of the reasoning strategy to retrieve. Defaults to None.
        :param reasoning_strategy_name: str, optional - Name of the reasoning strategy to retrieve. Defaults to None.
        :return: dict or str - JSON response containing the reasoning strategy details if successful, otherwise the raw response text.
        :raises ValueError: If neither reasoning_strategy_id nor reasoning_strategy_name is provided.
        """
        if not (reasoning_strategy_id or reasoning_strategy_name):
            raise ValueError("Either reasoning_strategy_id or reasoning_strategy_name must be provided.")

        identifier = reasoning_strategy_id if reasoning_strategy_id else reasoning_strategy_name
        endpoint = GET_REASONING_STRATEGY_V2.format(reasoningStrategyId=identifier)

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        if reasoning_strategy_id:
            logger.debug(f"Retrieving reasoning strategy detail with ID {reasoning_strategy_id}")
        else:
            logger.debug(f"Retrieving reasoning strategy detail with name {reasoning_strategy_name}")

        response = self.api_service.get(
            endpoint=endpoint,
            headers=headers
        )
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result