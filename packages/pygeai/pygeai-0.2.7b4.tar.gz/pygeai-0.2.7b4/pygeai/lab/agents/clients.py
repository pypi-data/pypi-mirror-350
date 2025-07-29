from json import JSONDecodeError
from typing import Optional, List, Dict

from pygeai import logger
from pygeai.core.base.clients import BaseClient
from pygeai.lab.agents.endpoints import CREATE_AGENT_V2, LIST_AGENTS_V2, GET_AGENT_V2, CREATE_SHARING_LINK_V2, \
    PUBLISH_AGENT_REVISION_V2, DELETE_AGENT_V2, UPDATE_AGENT_V2, UPSERT_AGENT_V2


class AgentClient(BaseClient):

    def list_agents(
            self,
            project_id: str,
            status: str = "",
            start: int = "",
            count: int = "",
            access_scope: str = "public",
            allow_drafts: bool = True,
            allow_external: bool = False
    ):
        """
        Retrieves a list of agents associated with the specified project.

        :param project_id: str - Unique identifier of the project.
        :param status: str - Status of the agents to filter by. Defaults to "" (no filtering).
        :param start: int - Starting index for pagination. Defaults to "" (no offset).
        :param count: int - Number of agents to retrieve. Defaults to "" (no limit).
        :param access_scope: str - Access scope of the agents, either "public" or "private". Defaults to "public".
        :param allow_drafts: bool - Whether to include draft agents. Defaults to True.
        :param allow_external: bool - Whether to include external agents. Defaults to False.
        :return: dict or str - JSON response containing the list of agents if successful, otherwise the raw response text.
        """
        endpoint = LIST_AGENTS_V2
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        logger.debug(f"Listing agents for project with ID {project_id}")

        response = self.api_service.get(
            endpoint=endpoint,
            headers=headers,
            params={
                "status": status,
                "start": start,
                "count": count,
                "accessScope": access_scope,
                "allowDrafts": allow_drafts,
                "allowExternal": allow_external
            }
        )
        try:
            result = response.json()
        except JSONDecodeError as e:
            result = response.text

        return result

    def create_agent(
            self,
            project_id: str,
            name: str,
            access_scope: str,
            public_name: str,
            job_description: str,
            avatar_image: str,
            description: str,
            agent_data_prompt: dict,
            agent_data_llm_config: dict,
            agent_data_models: list,
            agent_data_resource_pools: Optional[List[Dict]] = None,
            automatic_publish: bool = False
    ) -> dict:
        """
        Creates a new agent in the specified project.

        :param project_id: str - Unique identifier of the project where the agent will be created.
        :param name: str - Name of the agent. Must be non-empty, unique within the project, and exclude ':' or '/'.
        :param access_scope: str - Access scope of the agent. Must be either 'public' or 'private'. Defaults to 'private'.
        :param public_name: str - Public name of the agent, required if access_scope is 'public'. Must be unique within the installation and follow a domain/library convention (e.g., 'com.example.my-agent'). Only alphanumeric characters, periods, dashes, and underscores are allowed. Optional if access_scope is 'private'.
        :param job_description: str - Description of the agent's role. Optional.
        :param avatar_image: str - URL from which the agent's avatar image will be loaded. Optional.
        :param description: str - Detailed description of the agent’s purpose. Optional.
        :param agent_data_prompt: dict - Configuration for the agent's prompt. Must include at least 'context' or 'instructions' for publication. Optional fields include 'examples' with 'inputData' and 'output' pairs. Example structure:
            {
                'context': str,
                'instructions': str,
                'examples': [{'inputData': str, 'output': str}, ...]
            }
        :param agent_data_llm_config: dict - Default LLM configuration for the agent. Optional. Example structure:
            {
                'maxTokens': int,  # Maximum tokens for generation
                'timeout': int,    # Timeout in seconds
                'sampling': {
                    'temperature': float  # Controls randomness (0.0 to 1.0)
                }
            }
        :param agent_data_models: list - List of models the agent can use, in order of preference. At least one valid model is required for publication. Each model is a dict with 'name' (e.g., 'gpt-4o' or 'openai/gpt-4o') and optional 'llmConfig' to override defaults. Example:
            [{'name': str, 'llmConfig': dict}, ...]
        :param agent_data_resource_pools: Optional[List[Dict]] - List of resource pools organizing tools and helper agents. Optional. Each pool is a dict with 'name' (required), and optional 'tools' and 'agents' lists. Example structure:
        [
            {
                'name': str,
                'tools': [{'name': str, 'revision': int}, ...],
                'agents': [{'name': str, 'revision': int}, ...]
            },
            ...
        ]
        :param automatic_publish: bool - If True, automatically publishes the agent after creation. Defaults to False.
        :return: dict - JSON response containing the created agent details if successful, otherwise the raw response text.
        :raises JSONDecodeError: If the response cannot be parsed as JSON.
        """
        data = {
            "agentDefinition": {
                "name": name,
                "accessScope": access_scope,
                "publicName": public_name,
                "jobDescription": job_description,
                "avatarImage": avatar_image,
                "description": description,
                "agentData": {
                    "prompt": agent_data_prompt,
                    "llmConfig": agent_data_llm_config,
                    "models": agent_data_models
                }
            }
        }

        if agent_data_resource_pools is not None:
            data["agentDefinition"]["agentData"]["resourcePools"] = agent_data_resource_pools

        logger.debug(f"Creating agent with data: {data}")

        endpoint = CREATE_AGENT_V2
        if automatic_publish:
            endpoint = f"{endpoint}?automaticPublish=true"

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        response = self.api_service.post(
            endpoint=endpoint,
            headers=headers,
            data=data
        )

        try:
            result = response.json()
        except JSONDecodeError as e:
            result = response.text

        return result

    def get_agent(
            self,
            project_id: str,
            agent_id: str,
            revision: str = 0,
            version: int = 0,
            allow_drafts: bool = True
    ):
        """
        Retrieves details of a specific agent from the specified project.

        :param project_id: str - Unique identifier of the project.
        :param agent_id: str - Unique identifier of the agent to retrieve.
        :param revision: str - Revision of the agent to retrieve. Defaults to 0 (latest revision).
        :param version: int - Version of the agent to retrieve. Defaults to 0 (latest version).
        :param allow_drafts: bool - Whether to include draft agents in the retrieval. Defaults to True.
        :return: dict or str - JSON response containing the agent details if successful, otherwise the raw response text.
        """
        endpoint = GET_AGENT_V2.format(agentId=agent_id)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        logger.debug(f"Retrieving agent detail with ID {agent_id}")

        response = self.api_service.get(
            endpoint=endpoint,
            headers=headers,
            params={
                "revision": revision,
                "version": version,
                "allowDrafts": allow_drafts,
            }
        )
        try:
            result = response.json()
        except JSONDecodeError as e:
            result = response.text

        return result

    def create_sharing_link(
            self,
            project_id: str,
            agent_id: str,
    ):
        """
        Creates a sharing link for a specific agent in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param agent_id: str - Unique identifier of the agent for which to create a sharing link.
        :return: dict or str - JSON response containing the sharing link details if successful, otherwise the raw response text.
        """
        endpoint = CREATE_SHARING_LINK_V2.format(agentId=agent_id)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        logger.debug(f"Creating sharing link for agent with ID {agent_id}")

        response = self.api_service.get(
            endpoint=endpoint,
            headers=headers,
            params={}
        )
        try:
            result = response.json()
        except JSONDecodeError as e:
            result = response.text

        return result

    def publish_agent_revision(
            self,
            project_id: str,
            agent_id: str,
            revision: str
    ):
        """
        Publishes a specific revision of an agent in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param agent_id: str - Unique identifier of the agent to publish.
        :param revision: str - Revision of the agent to publish.
        :return: dict or str - JSON response containing the result of the publish operation if successful, otherwise the raw response text.
        """
        endpoint = PUBLISH_AGENT_REVISION_V2.format(agentId=agent_id)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        logger.debug(f"Publishing revision {revision} for agent with ID {agent_id}")

        response = self.api_service.post(
            endpoint=endpoint,
            headers=headers,
            data={
                "revision": revision,
            }
        )
        try:
            result = response.json()
        except JSONDecodeError as e:
            result = response.text

        return result

    def delete_agent(
            self,
            project_id: str,
            agent_id: str,
    ):
        """
        Deletes a specific agent from the specified project.

        :param project_id: str - Unique identifier of the project.
        :param agent_id: str - Unique identifier of the agent to delete.
        :return: dict or str - JSON response confirming the deletion if successful, otherwise the raw response text.
        """
        endpoint = DELETE_AGENT_V2.format(agentId=agent_id)
        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        logger.debug(f"Deleting agent with ID {agent_id}")

        response = self.api_service.delete(
            endpoint=endpoint,
            headers=headers,
            data={}
        )
        try:
            result = response.json()
        except JSONDecodeError as e:
            result = response.text

        return result

    def update_agent(
            self,
            project_id: str,
            agent_id: str,
            name: str,
            access_scope: str,
            public_name: str,
            job_description: str,
            avatar_image: str,
            description: str,
            agent_data_prompt: dict,
            agent_data_llm_config: dict,
            agent_data_models: list,
            agent_data_resource_pools: Optional[List[Dict]] = None,
            automatic_publish: bool = False,
            upsert: bool = False
    ) -> dict:
        """
        Updates an existing agent in the specified project or upserts it if specified.

        :param project_id: str - Unique identifier of the project containing the agent.
        :param agent_id: str - Unique identifier of the agent to update. Required for update operations.
        :param name: str - Updated name of the agent. Must be non-empty, unique within the project, and exclude ':' or '/' if provided. Optional.
        :param access_scope: str - Updated access scope of the agent. Must be either 'public' or 'private'. Defaults to 'private'.
        :param public_name: str - Updated public name of the agent, required if access_scope is 'public'. Must be unique within the installation and follow a domain/library convention (e.g., 'com.example.my-agent'). Only alphanumeric characters, periods, dashes, and underscores are allowed. Optional if access_scope is 'private'.
        :param job_description: str - Updated description of the agent's role. Optional.
        :param avatar_image: str - Updated URL from which the agent's avatar image will be loaded. Optional.
        :param description: str - Updated detailed description of the agent’s purpose. Optional.
        :param agent_data_prompt: dict - Updated configuration for the agent's prompt. Must include at least 'context' or 'instructions' for publication. Optional fields include 'examples' with 'inputData' and 'output' pairs. Optional. Example structure:
            {
                'context': str,
                'instructions': str,
                'examples': [{'inputData': str, 'output': str}, ...]
            }
        :param agent_data_llm_config: dict - Updated default LLM configuration for the agent. Optional. Example structure:
            {
                'maxTokens': int,  # Maximum tokens for generation
                'timeout': int,    # Timeout in seconds
                'sampling': {
                    'temperature': float  # Controls randomness (0.0 to 1.0)
                }
            }
        :param agent_data_models: list - Updated list of models the agent can use, in order of preference. At least one valid model is required for publication. Each model is a dict with 'name' (e.g., 'gpt-4o' or 'openai/gpt-4o') and optional 'llmConfig' to override defaults. Optional. Example:
            [{'name': str, 'llmConfig': dict}, ...]
        :param agent_data_resource_pools: Optional[List[Dict]] - Updated list of resource pools organizing tools and helper agents. Optional. Each pool is a dict with 'name' (required), and optional 'tools' and 'agents' lists. Example structure:
        [
            {
                'name': str,
                'tools': [{'name': str, 'revision': int}, ...],
                'agents': [{'name': str, 'revision': int}, ...]
            },
            ...
        ]
        :param automatic_publish: bool - If True, automatically publishes the agent after updating. Defaults to False.
        :param upsert: bool - If True, creates the agent if it does not exist (upsert); otherwise, only updates an existing agent. Defaults to False.
        :return: dict - JSON response containing the updated or created agent details if successful, otherwise the raw response text.
        :raises JSONDecodeError: If the response cannot be parsed as JSON.
        """
        data = {
            "agentDefinition": {
                "name": name,
                "accessScope": access_scope,
                "publicName": public_name,
                "jobDescription": job_description,
                "avatarImage": avatar_image,
                "description": description,
                "agentData": {
                    "prompt": agent_data_prompt,
                    "llmConfig": agent_data_llm_config,
                    "models": agent_data_models
                }
            }
        }
        if agent_data_resource_pools is not None:
            data["agentDefinition"]["agentData"]["resourcePools"] = agent_data_resource_pools

        logger.debug(f"Updating agent with ID {agent_id} with data: {data}")

        endpoint = UPSERT_AGENT_V2 if upsert else UPDATE_AGENT_V2
        endpoint = endpoint.format(agentId=agent_id) if agent_id else endpoint.format(agentId=name)

        if automatic_publish:
            endpoint = f"{endpoint}?automaticPublish=true"

        headers = {
            "Authorization": self.api_service.token,
            "ProjectId": project_id
        }

        response = self.api_service.put(
            endpoint=endpoint,
            headers=headers,
            data=data
        )

        try:
            result = response.json()
        except JSONDecodeError as e:
            result = response.text

        return result
