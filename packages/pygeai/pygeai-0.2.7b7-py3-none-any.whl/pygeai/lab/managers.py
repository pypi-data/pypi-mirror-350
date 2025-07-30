from typing import Union, Optional, List

from pygeai.core.base.mappers import ResponseMapper
from pygeai.core.base.responses import ErrorListResponse, EmptyResponse
from pygeai.core.handlers import ErrorHandler
from pygeai.lab.agents.clients import AgentClient
from pygeai.lab.agents.mappers import AgentMapper
from pygeai.lab.models import FilterSettings, Agent, AgentList, SharingLink, Tool, ToolList, ToolParameter, \
    ReasoningStrategyList, ReasoningStrategy, AgenticProcess, AgenticProcessList, ProcessInstanceList, Task, TaskList, \
    ProcessInstance, Variable, VariableList, KnowledgeBase, KnowledgeBaseList, JobList
from pygeai.lab.processes.clients import AgenticProcessClient
from pygeai.lab.processes.mappers import AgenticProcessMapper, ProcessInstanceMapper, TaskMapper, KnowledgeBaseMapper, \
    JobMapper
from pygeai.lab.strategies.clients import ReasoningStrategyClient
from pygeai.lab.strategies.mappers import ReasoningStrategyMapper
from pygeai.lab.tools.clients import ToolClient
from pygeai.lab.tools.mappers import ToolMapper


class AILabManager:

    def __init__(self, api_key: str = None, base_url: str = None, alias: str = "default"):
        self.__agent_client = AgentClient(api_key=api_key, base_url=base_url, alias=alias)
        self.__tool_client = ToolClient(api_key=api_key, base_url=base_url, alias=alias)
        self.__reasoning_strategy_client = ReasoningStrategyClient(api_key=api_key, base_url=base_url, alias=alias)
        self.__process_client = AgenticProcessClient(api_key=api_key, base_url=base_url, alias=alias)

    def get_agent_list(
            self,
            project_id: str,
            filter_settings: FilterSettings = None
    ) -> AgentList:
        """
        Retrieves a list of agents for a given project based on filter settings.

        This method queries the agent client to fetch a list of agents associated with the specified
        project ID, applying the provided filter settings. If the response contains errors, it maps
        them to an `ErrorListResponse`. Otherwise, it maps the response to an `AgentList`.

        :param project_id: str - The ID of the project to retrieve agents for.
        :param filter_settings: FilterSettings - The filter settings to apply to the agent list query.
            Includes fields such as status, start, count, access_scope, allow_drafts, and allow_external.
        :return: Union[AgentList, ErrorListResponse] - An `AgentList` containing the retrieved agents
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        if not filter_settings:
            filter_settings = FilterSettings()

        response_data = self.__agent_client.list_agents(
            project_id=project_id,
            status=filter_settings.status,
            start=filter_settings.start,
            count=filter_settings.count,
            access_scope=filter_settings.access_scope,
            allow_drafts=filter_settings.allow_drafts,
            allow_external=filter_settings.allow_external
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = AgentMapper.map_to_agent_list(response_data)

        return result

    def create_agent(
            self,
            project_id: str,
            agent: Agent,
            automatic_publish: bool = False
    ) -> Union[Agent, ErrorListResponse]:
        """
        Creates a new agent in the specified project using the provided agent configuration.

        This method sends a request to the agent client to create an agent based on the attributes
        of the provided `Agent` object. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to an `Agent` object.

        :param project_id: str - Unique identifier of the project where the agent will be created.
        :param agent: Agent - The agent configuration object containing all necessary details,
            including name, access scope, public name, job description, avatar image, description,
            and agent data (prompt, LLM config, and models).
        :param automatic_publish: bool - Whether to automatically publish the agent after creation.
            Defaults to False.
        :return: Union[Agent, ErrorListResponse] - An `Agent` object representing the created agent
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__agent_client.create_agent(
            project_id=project_id,
            name=agent.name,
            access_scope=agent.access_scope,
            public_name=agent.public_name,
            job_description=agent.job_description,
            avatar_image=agent.avatar_image,
            description=agent.description,
            agent_data_prompt=agent.agent_data.prompt.to_dict() if agent.agent_data is not None else None,
            agent_data_llm_config=agent.agent_data.llm_config.to_dict() if agent.agent_data is not None else None,
            agent_data_models=agent.agent_data.models.to_dict() if agent.agent_data is not None else None,
            agent_data_resource_pools=agent.agent_data.resource_pools.to_dict() if agent.agent_data and agent.agent_data.resource_pools else None,
            automatic_publish=automatic_publish
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = AgentMapper.map_to_agent(response_data)

        return result

    def update_agent(
            self,
            project_id: str,
            agent: Agent,
            automatic_publish: bool = False,
            upsert: bool = False
    ) -> Union[Agent, ErrorListResponse]:
        """
        Updates an existing agent in the specified project using the provided agent configuration.

        This method sends a request to the agent client to update an agent identified by `agent_id`
        (or `agent.id` if not provided) based on the attributes of the provided `Agent` object.
        It can optionally publish the agent automatically or perform an upsert if the agent doesn’t exist.
        If the response contains errors, it maps them to an `ErrorListResponse`. Otherwise, it maps
        the response to an `Agent` object.

        :param project_id: str - Unique identifier of the project where the agent resides.
        :param agent: Agent - The agent configuration object containing updated details,
            including id, name, access scope, public name, job description, avatar image, description,
            and agent data (prompt, LLM config, and models).
        :param automatic_publish: bool - Whether to automatically publish the agent after updating.
            Defaults to False.
        :param upsert: bool - Whether to insert the agent if it does not exist (upsert) instead of
            just updating. Defaults to False.
        :return: Union[Agent, ErrorListResponse] - An `Agent` object representing the updated agent
            if successful, or an `ErrorListResponse` if the API returns errors.
        :raises ValueError: If neither `agent_id` nor `agent.id` is provided.
        """
        response_data = self.__agent_client.update_agent(
            project_id=project_id,
            agent_id=agent.id,
            name=agent.name,
            access_scope=agent.access_scope,
            public_name=agent.public_name,
            job_description=agent.job_description,
            avatar_image=agent.avatar_image,
            description=agent.description,
            agent_data_prompt=agent.agent_data.prompt.to_dict() if agent.agent_data is not None else None,
            agent_data_llm_config=agent.agent_data.llm_config.to_dict() if agent.agent_data is not None else None,
            agent_data_models=agent.agent_data.models.to_dict() if agent.agent_data is not None else None,
            automatic_publish=automatic_publish,
            upsert=upsert
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = AgentMapper.map_to_agent(response_data)

        return result

    def get_agent(
            self,
            project_id: str,
            agent_id: str,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[Agent, ErrorListResponse]:
        """
        Retrieves details of a specific agent from the specified project.

        This method sends a request to the agent client to retrieve an agent identified by `agent_id`
        from the specified project. Optional filter settings can be provided to specify the revision,
        version, and whether to allow drafts. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to an `Agent` object.

        :param project_id: str - Unique identifier of the project where the agent resides.
        :param agent_id: str - Unique identifier of the agent to retrieve.
        :param filter_settings: FilterSettings, optional - Settings to filter the agent retrieval,
            including revision (defaults to "0"), version (defaults to 0), and allow_drafts (defaults to True).
        :return: Union[Agent, ErrorListResponse] - An `Agent` object representing the retrieved agent
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        if filter_settings is None:
            filter_settings = FilterSettings(
                revision="0",
                version="0",
                allow_drafts=True
            )

        response_data = self.__agent_client.get_agent(
            project_id=project_id,
            agent_id=agent_id,
            revision=filter_settings.revision,
            version=filter_settings.version,
            allow_drafts=filter_settings.allow_drafts
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = AgentMapper.map_to_agent(response_data)

        return result

    def create_sharing_link(
            self,
            project_id: str,
            agent_id: str
    ) -> Union[SharingLink, ErrorListResponse]:
        """
        Creates a sharing link for a specific agent in the specified project.

        This method sends a request to the agent client to create a sharing link for the agent
        identified by `agent_id` in the specified project. If the response contains errors, it maps
        them to an `ErrorListResponse`. Otherwise, it maps the response to a `SharingLink` object.

        :param project_id: str - Unique identifier of the project where the agent resides.
        :param agent_id: str - Unique identifier of the agent for which to create a sharing link.
        :return: Union[SharingLink, ErrorListResponse] - A `SharingLink` object representing the
            sharing link details if successful, or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__agent_client.create_sharing_link(
            project_id=project_id,
            agent_id=agent_id
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = AgentMapper.map_to_sharing_link(response_data)

        return result

    def publish_agent_revision(
            self,
            project_id: str,
            agent_id: str,
            revision: str
    ) -> Union[Agent, ErrorListResponse]:
        """
        Publishes a specific revision of an agent in the specified project.

        This method sends a request to the agent client to publish the specified revision of the agent
        identified by `agent_id` in the specified project. If the response contains errors, it maps
        them to an `ErrorListResponse`. Otherwise, it maps the response to an `Agent` object
        representing the published agent.

        :param project_id: str - Unique identifier of the project where the agent resides.
        :param agent_id: str - Unique identifier of the agent to publish.
        :param revision: str - Revision of the agent to publish.
        :return: Union[Agent, ErrorListResponse] - An `Agent` object representing the published agent
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__agent_client.publish_agent_revision(
            project_id=project_id,
            agent_id=agent_id,
            revision=revision
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = AgentMapper.map_to_agent(response_data)

        return result

    def delete_agent(
            self,
            project_id: str,
            agent_id: str
    ) -> Union[EmptyResponse, ErrorListResponse]:
        """
        Deletes a specific agent from the specified project.

        This method sends a request to the agent client to delete the agent identified by `agent_id`
        from the specified project. Returns True if the deletion is successful (indicated by an
        empty response or success confirmation), or an `ErrorListResponse` if the API returns errors.

        :param project_id: str - Unique identifier of the project where the agent resides.
        :param agent_id: str - Unique identifier of the agent to delete.
        :return: Union[EmptyResponse, ErrorListResponse] - EmptyResponse if the agent was deleted successfully,
            or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__agent_client.delete_agent(
            project_id=project_id,
            agent_id=agent_id
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            response_data = response_data if response_data else "Agent deleted successfully"
            result = ResponseMapper.map_to_empty_response(response_data)

        return result

    def create_tool(
            self,
            project_id: str,
            tool: Tool,
            automatic_publish: bool = False
    ) -> Union[Tool, ErrorListResponse]:
        """
        Creates a new tool in the specified project using the provided tool configuration.

        This method sends a request to the tool client to create a tool based on the attributes
        of the provided `Tool` object, including name, description, scope, access_scope, public_name,
        icon, open_api, open_api_json, report_events, and parameters. If the response contains errors,
        it maps them to an `ErrorListResponse`. Otherwise, it maps the response to a `Tool` object.

        :param project_id: str - Unique identifier of the project where the tool will be created.
        :param tool: Tool - The tool configuration object containing name, description, scope,
            access_scope, public_name, icon, open_api, open_api_json, report_events, and parameters.
            Optional fields (e.g., id, access_scope) are included if set in the `Tool` object.
        :param automatic_publish: bool - Whether to automatically publish the tool after creation.
            Defaults to False.
        :return: Union[Tool, ErrorListResponse] - A `Tool` object representing the created tool
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        parameters = [param.to_dict() for param in tool.parameters] if tool.parameters else []

        response_data = self.__tool_client.create_tool(
            project_id=project_id,
            name=tool.name,
            description=tool.description,
            scope=tool.scope,
            access_scope=tool.access_scope,
            public_name=tool.public_name,
            icon=tool.icon,
            open_api=tool.open_api,
            open_api_json=tool.open_api_json,
            report_events=tool.report_events,
            parameters=parameters,
            automatic_publish=automatic_publish
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ToolMapper.map_to_tool(response_data)

        return result

    def update_tool(
            self,
            project_id: str,
            tool: Tool,
            automatic_publish: bool = False,
            upsert: bool = False
    ) -> Union[Tool, ErrorListResponse]:
        """
        Updates an existing tool in the specified project or upserts it if specified.

        This method sends a request to the tool client to update a tool identified by `tool.id`
        based on the attributes of the provided `Tool` object, including name, description, scope,
        access_scope, public_name, icon, open_api, open_api_json, report_events, and parameters.
        It can optionally publish the tool automatically or perform an upsert if the tool doesn’t exist.
        If the response contains errors, it maps them to an `ErrorListResponse`. Otherwise, it maps
        the response to a `Tool` object.

        :param project_id: str - Unique identifier of the project where the tool resides.
        :param tool: Tool - The tool configuration object containing updated details, including
            id, name, description, scope, access_scope, public_name, icon, open_api, open_api_json,
            report_events, and parameters.
        :param automatic_publish: bool - Whether to automatically publish the tool after updating.
            Defaults to False.
        :param upsert: bool - Whether to insert the tool if it does not exist (upsert) instead of
            just updating. Defaults to False.
        :return: Union[Tool, ErrorListResponse] - A `Tool` object representing the updated tool
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        parameters = [param.to_dict() for param in tool.parameters] if tool.parameters else []

        response_data = self.__tool_client.update_tool(
            project_id=project_id,
            tool_id=tool.id,
            name=tool.name,
            description=tool.description,
            scope=tool.scope,
            access_scope=tool.access_scope,
            public_name=tool.public_name,
            icon=tool.icon,
            open_api=tool.open_api,
            open_api_json=tool.open_api_json,
            report_events=tool.report_events,
            parameters=parameters,
            automatic_publish=automatic_publish,
            upsert=upsert
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ToolMapper.map_to_tool(response_data)

        return result

    def get_tool(
            self,
            project_id: str,
            tool_id: str,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[Tool, ErrorListResponse]:
        """
        Retrieves details of a specific tool from the specified project.

        This method sends a request to the tool client to retrieve a tool identified by `tool_id`
        from the specified project. Optional filter settings can be provided to specify the revision,
        version, and whether to allow drafts. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to a `Tool` object.

        :param project_id: str - Unique identifier of the project where the tool resides.
        :param tool_id: str - Unique identifier of the tool to retrieve.
        :param filter_settings: FilterSettings, optional - Settings to filter the tool retrieval,
            including revision (defaults to "0"), version (defaults to "0"), and allow_drafts (defaults to True).
        :return: Union[Tool, ErrorListResponse] - A `Tool` object representing the retrieved tool
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        if filter_settings is None:
            filter_settings = FilterSettings(
                revision="0",
                version="0",
                allow_drafts=True
            )

        response_data = self.__tool_client.get_tool(
            project_id=project_id,
            tool_id=tool_id,
            revision=filter_settings.revision,
            version=filter_settings.version,
            allow_drafts=filter_settings.allow_drafts
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ToolMapper.map_to_tool(response_data)

        return result

    def delete_tool(
            self,
            project_id: str,
            tool_id: Optional[str] = None,
            tool_name: Optional[str] = None
    ) -> Union[EmptyResponse, ErrorListResponse]:
        """
        Deletes a specific tool from the specified project.

        This method sends a request to the tool client to delete the tool identified by either
        `tool_id` or `tool_name`. Returns an `EmptyResponse` if the deletion is successful,
        or an `ErrorListResponse` if the API returns errors.

        :param project_id: str - Unique identifier of the project where the tool resides.
        :param tool_id: str, optional - Unique identifier of the tool to delete.
        :param tool_name: str, optional - Name of the tool to delete.
        :return: Union[EmptyResponse, ErrorListResponse] - `EmptyResponse` if the tool was deleted successfully,
            or an `ErrorListResponse` if the API returns errors.
        :raises ValueError: If neither tool_id nor tool_name is provided.
        """
        if not (tool_id or tool_name):
            raise ValueError("Either tool_id or tool_name must be provided.")

        response_data = self.__tool_client.delete_tool(
            project_id=project_id,
            tool_id=tool_id,
            tool_name=tool_name
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            response_data = response_data if response_data else "Tool deleted successfully"
            result = ResponseMapper.map_to_empty_response(response_data)

        return result

    def list_tools(
            self,
            project_id: str,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[ToolList, ErrorListResponse]:
        """
        Retrieves a list of tools associated with the specified project.

        This method queries the tool client to fetch a list of tools for the given project ID,
        applying the specified filter settings. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to a `ToolList` object using `ToolMapper`.

        :param project_id: str - Unique identifier of the project.
        :param filter_settings: FilterSettings, optional - Settings to filter the tool list query,
            including id (defaults to ""), count (defaults to "100"), access_scope (defaults to "public"),
            allow_drafts (defaults to True), scope (defaults to "api"), and allow_external (defaults to True).
        :return: Union[ToolList, ErrorListResponse] - A `ToolList` object containing the retrieved tools
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        if filter_settings is None:
            filter_settings = FilterSettings(
                id="",
                count="100",
                access_scope="public",
                allow_drafts=True,
                scope="api",
                allow_external=True
            )

        response_data = self.__tool_client.list_tools(
            project_id=project_id,
            id=filter_settings.id,
            count=filter_settings.count,
            access_scope=filter_settings.access_scope,
            allow_drafts=filter_settings.allow_drafts,
            scope=filter_settings.scope,
            allow_external=filter_settings.allow_external
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ToolMapper.map_to_tool_list(response_data)

        return result

    def publish_tool_revision(
            self,
            project_id: str,
            tool_id: str,
            revision: str
    ) -> Union[Tool, ErrorListResponse]:
        """
        Publishes a specific revision of a tool in the specified project.

        This method sends a request to the tool client to publish the specified revision of the tool
        identified by `tool_id`. If the response contains errors, it maps them to an `ErrorListResponse`.
        Otherwise, it maps the response to a `Tool` object representing the published tool.

        :param project_id: str - Unique identifier of the project where the tool resides.
        :param tool_id: str - Unique identifier of the tool to publish.
        :param revision: str - Revision of the tool to publish.
        :return: Union[Tool, ErrorListResponse] - A `Tool` object representing the published tool
            if successful, or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__tool_client.publish_tool_revision(
            project_id=project_id,
            tool_id=tool_id,
            revision=revision
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ToolMapper.map_to_tool(response_data)

        return result

    def get_parameter(
            self,
            project_id: str,
            tool_id: Optional[str] = None,
            tool_public_name: Optional[str] = None,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[List[ToolParameter], ErrorListResponse]:
        """
        Retrieves details of parameters for a specific tool in the specified project.

        This method sends a request to the tool client to retrieve parameters for a tool identified
        by either `tool_id` or `tool_public_name`. Optional filter settings can specify revision,
        version, and whether to allow drafts. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to a list of `ToolParameter` objects.

        :param project_id: str - Unique identifier of the project.
        :param tool_id: str, optional - Unique identifier of the tool whose parameters are to be retrieved.
        :param tool_public_name: str, optional - Public name of the tool whose parameters are to be retrieved.
        :param filter_settings: FilterSettings, optional - Settings to filter the parameter retrieval,
            including revision (defaults to "0"), version (defaults to "0"), and allow_drafts (defaults to True).
        :return: Union[List[ToolParameter], ErrorListResponse] - A list of `ToolParameter` objects if successful,
            or an `ErrorListResponse` if the API returns errors.
        :raises ValueError: If neither tool_id nor tool_public_name is provided.
        """
        if not (tool_id or tool_public_name):
            raise ValueError("Either tool_id or tool_public_name must be provided.")

        if filter_settings is None:
            filter_settings = FilterSettings(
                revision="0",
                version="0",
                allow_drafts=True
            )

        response_data = self.__tool_client.get_parameter(
            project_id=project_id,
            tool_id=tool_id,
            tool_public_name=tool_public_name,
            revision=filter_settings.revision,
            version=filter_settings.version,
            allow_drafts=filter_settings.allow_drafts
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ToolMapper.map_to_parameter_list(response_data)

        return result

    def set_parameter(
            self,
            project_id: str,
            tool_id: Optional[str] = None,
            tool_public_name: Optional[str] = None,
            parameters: List[ToolParameter] = None
    ) -> Union[Tool, ErrorListResponse]:
        """
        Sets or updates parameters for a specific tool in the specified project.

        This method sends a request to the tool client to set parameters for a tool identified by
        either `tool_id` or `tool_public_name`. If the response contains errors, it maps them to an
        `ErrorListResponse`. Otherwise, it maps the response to a `Tool` object.

        :param project_id: str - Unique identifier of the project.
        :param tool_id: str, optional - Unique identifier of the tool whose parameters are to be set.
        :param tool_public_name: str, optional - Public name of the tool whose parameters are to be set.
        :param parameters: List[ToolParameter] - List of parameter objects defining the tool's parameters.
        :return: Union[Tool, ErrorListResponse] - A `Tool` object representing the updated tool if successful,
            or an `ErrorListResponse` if the API returns errors.
        :raises ValueError: If neither tool_id nor tool_public_name is provided, or if parameters is None or empty.
        """
        if not (tool_id or tool_public_name):
            raise ValueError("Either tool_id or tool_public_name must be provided.")
        if not parameters:
            raise ValueError("Parameters list must be provided and non-empty.")

        params_dict = [param.to_dict() for param in parameters]

        response_data = self.__tool_client.set_parameter(
            project_id=project_id,
            tool_id=tool_id,
            tool_public_name=tool_public_name,
            parameters=params_dict
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ResponseMapper.map_to_empty_response(response_data)

        return result

    def list_reasoning_strategies(
            self,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[ReasoningStrategyList, ErrorListResponse]:
        if filter_settings is None:
            filter_settings = FilterSettings(
                start="0",
                count="100",
                allow_external=True,
                access_scope="public"
            )

        response_data = self.__reasoning_strategy_client.list_reasoning_strategies(
            name=filter_settings.name or "",
            start=filter_settings.start,
            count=filter_settings.count,
            allow_external=filter_settings.allow_external,
            access_scope=filter_settings.access_scope
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ReasoningStrategyMapper.map_to_reasoning_strategy_list(response_data)

        return result

    def create_reasoning_strategy(
            self,
            project_id: str,
            strategy: ReasoningStrategy,
            automatic_publish: bool = False
    ) -> Union[ReasoningStrategy, ErrorListResponse]:
        response_data = self.__reasoning_strategy_client.create_reasoning_strategy(
            project_id=project_id,
            name=strategy.name,
            system_prompt=strategy.system_prompt,
            access_scope=strategy.access_scope,
            strategy_type=strategy.type,
            localized_descriptions=[desc.to_dict() for desc in strategy.localized_descriptions],
            automatic_publish=automatic_publish
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ReasoningStrategyMapper.map_to_reasoning_strategy(response_data)

        return result

    def update_reasoning_strategy(
            self,
            project_id: str,
            strategy: ReasoningStrategy,
            automatic_publish: bool = False,
            upsert: bool = False
    ) -> Union[ReasoningStrategy, ErrorListResponse]:
        response_data = self.__reasoning_strategy_client.update_reasoning_strategy(
            project_id=project_id,
            reasoning_strategy_id=strategy.id,
            name=strategy.name,
            system_prompt=strategy.system_prompt,
            access_scope=strategy.access_scope,
            strategy_type=strategy.type,
            localized_descriptions=[desc.to_dict() for desc in strategy.localized_descriptions],
            automatic_publish=automatic_publish,
            upsert=upsert
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ReasoningStrategyMapper.map_to_reasoning_strategy(response_data)

        return result

    def get_reasoning_strategy(
            self,
            project_id: str,
            reasoning_strategy_id: Optional[str] = None,
            reasoning_strategy_name: Optional[str] = None
    ) -> Union[ReasoningStrategy, ErrorListResponse]:
        if not (reasoning_strategy_id or reasoning_strategy_name):
            raise ValueError("Either reasoning_strategy_id or reasoning_strategy_name must be provided.")

        response_data = self.__reasoning_strategy_client.get_reasoning_strategy(
            project_id=project_id,
            reasoning_strategy_id=reasoning_strategy_id,
            reasoning_strategy_name=reasoning_strategy_name
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ReasoningStrategyMapper.map_to_reasoning_strategy(response_data)

        return result

    def create_process(
            self,
            project_id: str,
            process: AgenticProcess,
            automatic_publish: bool = False
    ) -> Union[AgenticProcess, ErrorListResponse]:
        """
        Creates a new process in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param process: AgenticProcess - The process configuration to create.
        :param automatic_publish: bool - Whether to publish the process after creation. Defaults to False.
        :return: Union[AgenticProcess, ErrorListResponse] - The created process if successful, or an error response.
        """
        response_data = self.__process_client.create_process(
            project_id=project_id,
            key=process.key,
            name=process.name,
            description=process.description,
            kb=process.kb.to_dict(),
            agentic_activities=[activity.to_dict() for activity in process.agentic_activities] if process.agentic_activities else None,
            artifact_signals=[signal.to_dict() for signal in process.artifact_signals] if process.artifact_signals else None,
            user_signals=[signal.to_dict() for signal in process.user_signals] if process.user_signals else None,
            start_event=process.start_event.to_dict(),
            end_event=process.end_event.to_dict(),
            sequence_flows=[flow.to_dict() for flow in process.sequence_flows] if process.sequence_flows else None,
            variables=[variable.to_dict() for variable in process.variables] if process.variables else None,
            automatic_publish=automatic_publish
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = AgenticProcessMapper.map_to_agentic_process(response_data)

        return result

    def update_process(
            self,
            project_id: str,
            process: AgenticProcess,
            automatic_publish: bool = False,
            upsert: bool = False
    ) -> Union[AgenticProcess, ErrorListResponse]:
        """
        Updates an existing process in the specified project or upserts it if specified.

        :param project_id: str - Unique identifier of the project.
        :param process: AgenticProcess - The process configuration to update.
        :param automatic_publish: bool - Whether to publish the process after updating. Defaults to False.
        :param upsert: bool - Whether to insert the process if it does not exist. Defaults to False.
        :return: Union[AgenticProcess, ErrorListResponse] - The updated process if successful, or an error response.
        """
        response_data = self.__process_client.update_process(
            project_id=project_id,
            process_id=process.id,
            name=process.name,
            key=process.key,
            description=process.description,
            kb=process.kb.to_dict(),
            agentic_activities=[activity.to_dict() for activity in process.agentic_activities] if process.agentic_activities else None,
            artifact_signals=[signal.to_dict() for signal in process.artifact_signals] if process.artifact_signals else None,
            user_signals=[signal.to_dict() for signal in process.user_signals] if process.user_signals else None,
            start_event=process.start_event.to_dict(),
            end_event=process.end_event.to_dict(),
            sequence_flows=[flow.to_dict() for flow in process.sequence_flows] if process.sequence_flows else None,
            variables=[variable.to_dict() for variable in process.variables] if process.variables else None,
            automatic_publish=automatic_publish,
            upsert=upsert
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = AgenticProcessMapper.map_to_agentic_process(response_data)

        return result

    def get_process(
            self,
            project_id: str,
            process_id: Optional[str] = None,
            process_name: Optional[str] = None,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[AgenticProcess, ErrorListResponse]:
        """
        Retrieves details of a specific process in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param process_id: Optional[str] - Unique identifier of the process to retrieve. Defaults to None.
        :param process_name: Optional[str] - Name of the process to retrieve. Defaults to None.
        :param filter_settings: Optional[FilterSettings] - Settings to filter the process retrieval (revision, version, allow_drafts).
        :return: Union[AgenticProcess, ErrorListResponse] - The retrieved process if successful, or an error response.
        :raises ValueError: If neither process_id nor process_name is provided.
        """
        if not (process_id or process_name):
            raise ValueError("Either process_id or process_name must be provided.")

        filter_settings = filter_settings or FilterSettings(revision="0", version="0", allow_drafts=True)
        response_data = self.__process_client.get_process(
            project_id=project_id,
            process_id=process_id,
            process_name=process_name,
            revision=filter_settings.revision,
            version=filter_settings.version,
            allow_drafts=filter_settings.allow_drafts
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = AgenticProcessMapper.map_to_agentic_process(response_data)

        return result

    def list_processes(
            self,
            project_id: str,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[AgenticProcessList, ErrorListResponse]:
        """
        Retrieves a list of processes in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param filter_settings: Optional[FilterSettings] - Settings to filter the process list (id, name, status, start, count, allow_drafts).
        :return: Union[AgenticProcessList, ErrorListResponse] - The list of processes if successful, or an error response.
        """
        filter_settings = filter_settings or FilterSettings(start="0", count="100", allow_drafts=True)
        response_data = self.__process_client.list_processes(
            project_id=project_id,
            id=filter_settings.id,
            name=filter_settings.name,
            status=filter_settings.status,
            start=filter_settings.start,
            count=filter_settings.count,
            allow_draft=filter_settings.allow_drafts
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = AgenticProcessMapper.map_to_agentic_process_list(response_data)

        return result

    def list_process_instances(
            self,
            project_id: str,
            process_id: str,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[ProcessInstanceList, ErrorListResponse]:
        """
        Retrieves a list of process instances for a specific process in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param process_id: str - Unique identifier of the process to list instances for.
        :param filter_settings: Optional[FilterSettings] - Settings to filter the instance list (is_active, start, count).
        :return: Union[ProcessInstanceList, ErrorListResponse] - The list of process instances if successful, or an error response.
        """
        filter_settings = filter_settings or FilterSettings(start="0", count="10", is_active=True)
        response_data = self.__process_client.list_process_instances(
            project_id=project_id,
            process_id=process_id,
            is_active=filter_settings.is_active,
            start=filter_settings.start,
            count=filter_settings.count
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ProcessInstanceMapper.map_to_process_instance_list(response_data)

        return result

    def delete_process(
            self,
            project_id: str,
            process_id: Optional[str] = None,
            process_name: Optional[str] = None
    ) -> Union[EmptyResponse, ErrorListResponse]:
        """
        Deletes a specific process in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param process_id: Optional[str] - Unique identifier of the process to delete. Defaults to None.
        :param process_name: Optional[str] - Name of the process to delete. Defaults to None.
        :return: Union[EmptyResponse, ErrorListResponse] - Empty response if successful, or an error response.
        :raises ValueError: If neither process_id nor process_name is provided.
        """
        if not (process_id or process_name):
            raise ValueError("Either process_id or process_name must be provided.")

        response_data = self.__process_client.delete_process(
            project_id=project_id,
            process_id=process_id,
            process_name=process_name
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ResponseMapper.map_to_empty_response(response_data or "Process deleted successfully")

        return result

    def publish_process_revision(
            self,
            project_id: str,
            process_id: Optional[str] = None,
            process_name: Optional[str] = None,
            revision: str = None
    ) -> Union[AgenticProcess, ErrorListResponse]:
        """
        Publishes a specific revision of a process in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param process_id: Optional[str] - Unique identifier of the process to publish. Defaults to None.
        :param process_name: Optional[str] - Name of the process to publish. Defaults to None.
        :param revision: str - Revision of the process to publish. Defaults to None.
        :return: Union[AgenticProcess, ErrorListResponse] - The published process if successful, or an error response.
        :raises ValueError: If neither process_id nor process_name is provided, or if revision is not specified.
        """
        if not (process_id or process_name) or not revision:
            raise ValueError("Either process_id or process_name and revision must be provided.")

        response_data = self.__process_client.publish_process_revision(
            project_id=project_id,
            process_id=process_id,
            process_name=process_name,
            revision=revision
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = AgenticProcessMapper.map_to_agentic_process(response_data)

        return result

    def create_task(
            self,
            project_id: str,
            task: Task,
            automatic_publish: bool = False
    ) -> Union[Task, ErrorListResponse]:
        """
        Creates a new task in the specified project.

        :param project_id: str - Unique identifier of the project where the task will be created.
        :param task: Task - The task configuration to create, including name (required), description,
            title_template, id, prompt_data, and artifact_types. Optional fields are included if set.
        :param automatic_publish: bool - Whether to publish the task after creation. Defaults to False.
        :return: Union[Task, ErrorListResponse] - The created task if successful, or an error response.
        """
        response_data = self.__process_client.create_task(
            project_id=project_id,
            name=task.name,
            description=task.description,
            title_template=task.title_template,
            id=task.id,
            prompt_data=task.prompt_data.to_dict() if task.prompt_data else None,
            artifact_types=task.artifact_types.to_dict() if task.artifact_types else None,
            automatic_publish=automatic_publish
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = TaskMapper.map_to_task(response_data)

        return result

    def get_task(
            self,
            project_id: str,
            task_id: Optional[str] = None,
            task_name: Optional[str] = None
    ) -> Union[Task, ErrorListResponse]:
        """
        Retrieves details of a specific task in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param task_id: Optional[str] - Unique identifier of the task to retrieve. Defaults to None.
        :param task_name: Optional[str] - Name of the task to retrieve. Defaults to None.
        :return: Union[Task, ErrorListResponse] - The retrieved task if successful, or an error response.
        :raises ValueError: If neither task_id nor task_name is provided.
        """
        if not (task_id or task_name):
            raise ValueError("Either task_id or task_name must be provided.")

        response_data = self.__process_client.get_task(
            project_id=project_id,
            task_id=task_id,
            task_name=task_name
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = TaskMapper.map_to_task(response_data)

        return result

    def list_tasks(
            self,
            project_id: str,
            filter_settings: Optional[FilterSettings] = None
    ) -> Union[TaskList, ErrorListResponse]:
        """
        Retrieves a list of tasks in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param filter_settings: Optional[FilterSettings] - Settings to filter the task list (id, start, count, allow_drafts).
        :return: Union[TaskList, ErrorListResponse] - The list of tasks if successful, or an error response.
        """
        filter_settings = filter_settings or FilterSettings(start="0", count="100", allow_drafts=True)
        response_data = self.__process_client.list_tasks(
            project_id=project_id,
            id=filter_settings.id,
            start=filter_settings.start,
            count=filter_settings.count,
            allow_drafts=filter_settings.allow_drafts
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = TaskMapper.map_to_task_list(response_data)

        return result

    def update_task(
            self,
            project_id: str,
            task: Task,
            automatic_publish: bool = False,
            upsert: bool = False
    ) -> Union[Task, ErrorListResponse]:
        """
        Updates an existing task in the specified project or upserts it if specified.

        :param project_id: str - Unique identifier of the project where the task resides.
        :param task: Task - The task configuration to update, including id (required), name, description,
            title_template, prompt_data, and artifact_types. Optional fields are included if set.
        :param automatic_publish: bool - Whether to publish the task after updating. Defaults to False.
        :param upsert: bool - Whether to insert the task if it does not exist. Defaults to False.
        :return: Union[Task, ErrorListResponse] - The updated task if successful, or an error response.
        :raises ValueError: If task.id is not provided.
        """
        if not task.id:
            raise ValueError("Task ID must be provided for update.")

        response_data = self.__process_client.update_task(
            project_id=project_id,
            task_id=task.id,
            name=task.name,
            description=task.description,
            title_template=task.title_template,
            id=task.id,
            prompt_data=task.prompt_data.to_dict() if task.prompt_data else None,
            artifact_types=task.artifact_types.to_dict() if task.artifact_types else None,
            automatic_publish=automatic_publish,
            upsert=upsert
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = TaskMapper.map_to_task(response_data)

        return result

    def delete_task(
            self,
            project_id: str,
            task_id: Optional[str] = None,
            task_name: Optional[str] = None
    ) -> Union[EmptyResponse, ErrorListResponse]:
        """
        Deletes a specific task in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param task_id: Optional[str] - Unique identifier of the task to delete. Defaults to None.
        :param task_name: Optional[str] - Name of the task to delete. Defaults to None.
        :return: Union[EmptyResponse, ErrorListResponse] - Empty response if successful, or an error response.
        :raises ValueError: If neither task_id nor task_name is provided.
        """
        if not (task_id or task_name):
            raise ValueError("Either task_id or task_name must be provided.")

        response_data = self.__process_client.delete_task(
            project_id=project_id,
            task_id=task_id,
            task_name=task_name
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ResponseMapper.map_to_empty_response(response_data or "Task deleted successfully")

        return result

    def publish_task_revision(
            self,
            project_id: str,
            task_id: Optional[str] = None,
            task_name: Optional[str] = None,
            revision: str = None
    ) -> Union[Task, ErrorListResponse]:
        """
        Publishes a specific revision of a task in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param task_id: Optional[str] - Unique identifier of the task to publish. Defaults to None.
        :param task_name: Optional[str] - Name of the task to publish. Defaults to None.
        :param revision: str - Revision of the task to publish. Defaults to None.
        :return: Union[Task, ErrorListResponse] - The published task if successful, or an error response.
        :raises ValueError: If neither task_id nor task_name is provided, or if revision is not specified.
        """
        if not (task_id or task_name) or not revision:
            raise ValueError("Either task_id or task_name and revision must be provided.")

        response_data = self.__process_client.publish_task_revision(
            project_id=project_id,
            task_id=task_id,
            task_name=task_name,
            revision=revision
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = TaskMapper.map_to_task(response_data)

        return result

    def start_instance(
            self,
            project_id: str,
            process_name: str,
            subject: Optional[str] = None,
            variables: Optional[List[Variable] | VariableList] = None
    ) -> Union[ProcessInstance, ErrorListResponse]:
        """
        Starts a new process instance in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param process_name: str - Name of the process to start an instance for.
        :param subject: Optional[str] - Subject of the process instance. Defaults to None.
        :param variables: Optional[List[dict]] - List of variables for the instance. Defaults to None.
        :return: Union[StartInstanceResponse, ErrorListResponse] - The started instance if successful, or an error response.
        """
        if not isinstance(variables, VariableList):
            variables = VariableList(variables=variables)

        response_data = self.__process_client.start_instance(
            project_id=project_id,
            process_name=process_name,
            subject=subject,
            variables=variables.to_dict()
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ProcessInstanceMapper.map_to_process_instance(response_data)

        return result

    def abort_instance(
            self,
            project_id: str,
            instance_id: str
    ) -> Union[EmptyResponse, ErrorListResponse]:
        """
        Aborts a specific process instance in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param instance_id: str - Unique identifier of the instance to abort.
        :return: Union[EmptyResponse, ErrorListResponse] - Empty response if successful, or an error response.
        :raises ValueError: If instance_id is not provided.
        """
        if not instance_id:
            raise ValueError("Instance ID must be provided.")

        response_data = self.__process_client.abort_instance(
            project_id=project_id,
            instance_id=instance_id
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ResponseMapper.map_to_empty_response(response_data or "Instance aborted successfully")

        return result

    def get_instance(
            self,
            project_id: str,
            instance_id: str
    ) -> Union[ProcessInstance, ErrorListResponse]:
        """
        Retrieves details of a specific process instance in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param instance_id: str - Unique identifier of the instance to retrieve.
        :return: Union[ProcessInstance, ErrorListResponse] - The retrieved instance if successful, or an error response.
        :raises ValueError: If instance_id is not provided.
        """
        if not instance_id:
            raise ValueError("Instance ID must be provided.")

        response_data = self.__process_client.get_instance(
            project_id=project_id,
            instance_id=instance_id
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ProcessInstanceMapper.map_to_process_instance(response_data)

        return result

    def get_instance_history(
            self,
            project_id: str,
            instance_id: str
    ) -> Union[dict, ErrorListResponse]:
        """
        Retrieves the history of a specific process instance in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param instance_id: str - Unique identifier of the instance to retrieve history for.
        :return: Union[dict, ErrorListResponse] - The instance history if successful, or an error response.
        :raises ValueError: If instance_id is not provided.
        """
        if not instance_id:
            raise ValueError("Instance ID must be provided.")

        response_data = self.__process_client.get_instance_history(
            project_id=project_id,
            instance_id=instance_id
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = response_data

        return result

    def get_thread_information(
            self,
            project_id: str,
            thread_id: str
    ) -> Union[dict, ErrorListResponse]:
        """
        Retrieves information about a specific thread in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param thread_id: str - Unique identifier of the thread to retrieve information for.
        :return: Union[dict, ErrorListResponse] - The thread information if successful, or an error response.
        :raises ValueError: If thread_id is not provided.
        """
        if not thread_id:
            raise ValueError("Thread ID must be provided.")

        response_data = self.__process_client.get_thread_information(
            project_id=project_id,
            thread_id=thread_id
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = response_data

        return result

    def send_user_signal(
            self,
            project_id: str,
            instance_id: str,
            signal_name: str
    ) -> Union[EmptyResponse, ErrorListResponse]:
        """
        Sends a user signal to a specific process instance in the specified project.

        :param project_id: str - Unique identifier of the project.
        :param instance_id: str - Unique identifier of the instance to send the signal to.
        :param signal_name: str - Name of the user signal to send.
        :return: Union[EmptyResponse, ErrorListResponse] - Empty response if successful, or an error response.
        :raises ValueError: If instance_id or signal_name is not provided.
        """
        if not instance_id or not signal_name:
            raise ValueError("Instance ID and signal name must be provided.")

        response_data = self.__process_client.send_user_signal(
            project_id=project_id,
            instance_id=instance_id,
            signal_name=signal_name
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ResponseMapper.map_to_empty_response(response_data or "Signal sent successfully")

        return result

    def create_knowledge_base(
            self,
            project_id: str,
            knowledge_base: KnowledgeBase,
    ) -> Union[KnowledgeBase, ErrorListResponse]:
        """
        Creates a new knowledge base in the specified project using the provided configuration.

        This method sends a request to the process client to create a knowledge base based on
        the attributes of the provided `KnowledgeBase` object. If the response contains errors, it
        maps them to an `ErrorListResponse`. Otherwise, it maps the response to a `KnowledgeBase` object.

        :param project_id: str - Unique identifier of the project where the knowledge base will be created.
        :param knowledge_base: KnowledgeBase - The knowledge base configuration object containing name
            and artifact type names.
        :return: Union[KnowledgeBase, ErrorListResponse] - A `KnowledgeBase` object representing the created
            knowledge base if successful, or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__process_client.create_kb(
            project_id=project_id,
            name=knowledge_base.name,
            artifacts=knowledge_base.artifacts if knowledge_base.artifacts else None,
            metadata=knowledge_base.metadata if knowledge_base.metadata else None
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = KnowledgeBaseMapper.map_to_knowledge_base(response_data)

        return result

    def list_knowledge_bases(
            self,
            project_id: str,
            name: Optional[str] = None,
            start: Optional[int] = 0,
            count: Optional[int] = 10
    ) -> Union[KnowledgeBaseList, ErrorListResponse]:
        """
        Retrieves a list of knowledge bases for the specified project.

        This method queries the process client to fetch a list of knowledge bases associated
        with the specified project ID, applying optional filters for name and pagination. If the
        response contains errors, it maps them to an `ErrorListResponse`. Otherwise, it maps the
        response to a `KnowledgeBaseList`.

        :param project_id: str - Unique identifier of the project to retrieve knowledge bases for.
        :param name: Optional[str] - Name filter to narrow down the list of knowledge bases.
        :param start: Optional[int] - Starting index for pagination, defaults to 0.
        :param count: Optional[int] - Number of knowledge bases to return, defaults to 10.
        :return: Union[KnowledgeBaseList, ErrorListResponse] - A `KnowledgeBaseList` containing the
            retrieved knowledge bases if successful, or an `ErrorListResponse` if the API returns errors.
        """
        response_data = self.__process_client.list_kbs(
            project_id=project_id,
            name=name,
            start=start,
            count=count
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = KnowledgeBaseMapper.map_to_knowledge_base_list(response_data)

        return result

    def get_knowledge_base(
            self,
            project_id: str,
            kb_name: Optional[str] = None,
            kb_id: Optional[str] = None
    ) -> Union[KnowledgeBase, ErrorListResponse]:
        """
        Retrieves details of a specific knowledge base from the specified project.

        This method sends a request to the process client to retrieve a knowledge base
        identified by either `kb_name` or `kb_id`. If the response contains errors, it maps them to
        an `ErrorListResponse`. Otherwise, it maps the response to a `KnowledgeBase` object.

        :param project_id: str - Unique identifier of the project where the knowledge base resides.
        :param kb_name: Optional[str] - Name of the knowledge base to retrieve.
        :param kb_id: Optional[str] - Unique identifier of the knowledge base to retrieve.
        :return: Union[KnowledgeBase, ErrorListResponse] - A `KnowledgeBase` object representing the
            retrieved knowledge base if successful, or an `ErrorListResponse` if the API returns errors.
        :raises ValueError: If neither `kb_name` nor `kb_id` is provided.
        """
        if not (kb_name or kb_id):
            raise ValueError("Either kb_name or kb_id must be provided.")

        response_data = self.__process_client.get_kb(
            project_id=project_id,
            kb_name=kb_name,
            kb_id=kb_id
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = KnowledgeBaseMapper.map_to_knowledge_base(response_data)

        return result

    def delete_knowledge_base(
            self,
            project_id: str,
            kb_name: Optional[str] = None,
            kb_id: Optional[str] = None
    ) -> Union[EmptyResponse, ErrorListResponse]:
        """
        Deletes a specific knowledge base from the specified project.

        This method sends a request to the process client to delete a knowledge base
        identified by either `kb_name` or `kb_id`. Returns an `EmptyResponse` if the deletion is
        successful, or an `ErrorListResponse` if the API returns errors.

        :param project_id: str - Unique identifier of the project where the knowledge base resides.
        :param kb_name: Optional[str] - Name of the knowledge base to delete.
        :param kb_id: Optional[str] - Unique identifier of the knowledge base to delete.
        :return: Union[EmptyResponse, ErrorListResponse] - `EmptyResponse` if the knowledge base was
            deleted successfully, or an `ErrorListResponse` if the API returns errors.
        :raises ValueError: If neither `kb_name` nor `kb_id` is provided.
        """
        if not (kb_name or kb_id):
            raise ValueError("Either kb_name or kb_id must be provided.")

        response_data = self.__process_client.delete_kb(
            project_id=project_id,
            kb_name=kb_name,
            kb_id=kb_id
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            response_data = response_data if response_data else "Knowledge base deleted successfully"
            result = ResponseMapper.map_to_empty_response(response_data)

        return result

    def list_jobs(
            self,
            project_id: str,
            filter_settings: Optional[FilterSettings] = None,
            topic: Optional[str] = None,
            token: Optional[str] = None
    ) -> Union[JobList, ErrorListResponse]:
        """
        Retrieves a list of jobs in the specified project.

        This method queries the process client to fetch a list of jobs associated with the specified
        project ID, applying optional filter settings. If the response contains errors,
        it maps them to an `ErrorListResponse`. Otherwise, it maps the response to a `JobList`.

        :param project_id: str - Unique identifier of the project.
        :param filter_settings: Optional[FilterSettings] - Settings to filter the job list (start, count).
        :param topic: Optional[str] - Topic to filter the jobs (e.g., 'Default', 'Event'). Defaults to None.
        :param token: Optional[str] - Unique token identifier to filter a specific job. Defaults to None.
        :return: Union[JobList, ErrorListResponse] - A `JobList` containing the retrieved jobs if successful,
            or an `ErrorListResponse` if the API returns errors.
        :raises ValueError: If project_id is not provided.
        """
        if not project_id:
            raise ValueError("Project ID must be provided.")

        filter_settings = filter_settings or FilterSettings(start="0", count="100")
        response_data = self.__process_client.list_jobs(
            project_id=project_id,
            start=filter_settings.start,
            count=filter_settings.count,
            topic=topic,
            token=token,
            name=filter_settings.name
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = JobMapper.map_to_job_list(response_data)

        return result
