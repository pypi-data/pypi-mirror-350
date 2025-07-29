from pygeai.core.base.mappers import ErrorMapper, ResponseMapper
from pygeai.core.handlers import ErrorHandler
from pygeai.core.models import Project
from pygeai.core.base.responses import EmptyResponse
from pygeai.organization.clients import OrganizationClient
from pygeai.organization.mappers import OrganizationResponseMapper
from pygeai.organization.responses import AssistantListResponse, ProjectListResponse, ProjectDataResponse, \
    ProjectTokensResponse, ProjectItemListResponse


class OrganizationManager:
    """
    Manager that operates as an abstraction level over the clients, designed to handle calls receiving and
    returning objects when appropriate.
    If errors are found in the response, they are processed using `ErrorMapper` to return a list of Errors.
    """

    def __init__(self, api_key: str = None, base_url: str = None, alias: str = "default"):
        self.__organization_client = OrganizationClient(api_key=api_key, base_url=base_url, alias=alias)

    def get_assistant_list(
            self,
            detail: str = "summary"
    ) -> AssistantListResponse:
        """
        Retrieves a list of assistants with the specified level of detail.

        This method calls `OrganizationClient.get_assistant_list` to fetch assistant data
        and maps the response using `OrganizationResponseMapper` into an `AssistantListResponse` object.

        :param detail: str - The level of detail to include in the response. Possible values:
            - "summary": Provides a summarized list of assistants. (Default)
            - "full": Provides a detailed list of assistants. (Optional)
        :return: AssistantListResponse - The mapped response containing the list of assistants.
        """
        response_data = self.__organization_client.get_assistant_list(detail=detail)
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = OrganizationResponseMapper.map_to_assistant_list_response(response_data)
            # TODO -> Add assistant list from plugins API
        return result

    def get_project_list(
            self,
            detail: str = "summary",
            name: str = None
    ) -> ProjectListResponse:
        """
        Retrieves a list of projects with the specified level of detail and optional filtering by name.

        This method calls `OrganizationClient.get_project_list` to fetch project data
        and maps the response using `OrganizationResponseMapper` into a `ProjectListResponse` object.

        :param detail: str - The level of detail to include in the response. Possible values:
            - "summary": Provides a summarized list of projects. (Default)
            - "full": Provides a detailed list of projects. (Optional)
        :param name: str, optional - Filters projects by name. If not provided, all projects are returned.
        :return: ProjectListResponse - The mapped response containing the list of projects or an error list.
        """
        response_data = self.__organization_client.get_project_list(
            detail=detail,
            name=name
            )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = OrganizationResponseMapper.map_to_project_list_response(response_data)
        return result

    def get_project_data(
            self,
            project_id: str
    ) -> ProjectDataResponse:
        """
        Retrieves detailed data for a specific project.

        This method calls `OrganizationClient.get_project_data` to fetch project details
        and maps the response using `OrganizationResponseMapper` into a `ProjectDataResponse` object.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param project_id: str - The unique identifier of the project to retrieve.
        :return: ProjectDataResponse - The mapped response containing project details or an error list.
        """
        response_data = self.__organization_client.get_project_data(
            project_id=project_id
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = OrganizationResponseMapper.map_to_project_data(response_data)
        return result

    def create_project(
            self,
            project: Project

    ):
        """
        Creates a new project with the given details and optional usage limit settings.

        This method calls `OrganizationClient.create_project` to create a new project and maps the response
        using `OrganizationResponseMapper` into a `ProjectDataResponse` object.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param project: Project - The project object containing details such as name, email, and description.
        :param usage_limit: UsageLimit, optional - Defines usage limits for the project, including subscription type,
                            unit, soft and hard limits, and renewal status. Defaults to None.
        :return: ProjectDataResponse - The mapped response containing the created project details or an error list.
        """
        response_data = self.__organization_client.create_project(
            name=project.name,
            email=project.email,
            description=project.description,
            usage_limit={
                "subscriptionType": project.usage_limit.subscription_type,
                "usageUnit": project.usage_limit.usage_unit,
                "softLimit": project.usage_limit.soft_limit,
                "hardLimit": project.usage_limit.hard_limit,
                "renewalStatus": project.usage_limit.renewal_status,
            } if project.usage_limit is not None else None,
        )

        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = OrganizationResponseMapper.map_to_project_data(response_data)

        return result

    def update_project(
            self,
            project: Project
    ):
        """
        Updates an existing project with the provided details.

        This method calls `OrganizationClient.update_project` to update project information and maps the response
        using `OrganizationResponseMapper` into a `ProjectDataResponse` object.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param project: Project - The project object containing updated details such as project ID, name, and description.
        :return: ProjectDataResponse - The mapped response containing the updated project details or an error list.
        """
        response_data = self.__organization_client.update_project(
            project_id=project.id,
            name=project.name,
            description=project.description
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = OrganizationResponseMapper.map_to_project_data(response_data)

        return result

    def delete_project(
            self,
            project_id: str
    ) -> EmptyResponse:
        """
        Deletes a project by its unique identifier.

        This method calls `OrganizationClient.delete_project` to remove a project and maps the response
        using `ResponseMapper.map_to_empty_response`.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param project_id: str - The unique identifier of the project to be deleted.
        :return: EmptyResponse - An empty response indicating successful deletion or an error list if the request fails.
        """
        response_data = self.__organization_client.delete_project(
            project_id=project_id
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ResponseMapper.map_to_empty_response(response_data)

        return result

    def get_project_tokens(
            self,
            project_id: str
    ) -> ProjectTokensResponse:
        """
        Retrieves a list of tokens associated with a specific project.

        This method calls `OrganizationClient.get_project_tokens` to fetch token data and maps the response
        using `OrganizationResponseMapper.map_to_token_list_response`.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param project_id: str - The unique identifier of the project whose tokens are to be retrieved.
        :return: ProjectTokensResponse - The mapped response containing the list of project tokens or an error list.
        """
        response_data = self.__organization_client.get_project_tokens(
            project_id=project_id
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = OrganizationResponseMapper.map_to_token_list_response(response_data)

        return result

    def export_request_data(
            self,
            assistant_name: str = None,
            status: str = None,
            skip: int = 0,
            count: int = 0
    ) -> ProjectItemListResponse:
        """
        Exports request data based on specified filters.

        This method calls `OrganizationClient.export_request_data` to retrieve request data
        filtered by assistant name, status, and pagination parameters. The response is mapped
        using `OrganizationResponseMapper.map_to_item_list_response`.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param assistant_name: str, optional - Filters requests by assistant name. If not provided, all assistants are included.
        :param status: str, optional - Filters requests by status. If not provided, all statuses are included.
        :param skip: int, optional - The number of records to skip for pagination. Default is 0.
        :param count: int, optional - The number of records to retrieve. Default is 0 (no limit).
        :return: ProjectItemListResponse - The mapped response containing the exported request data or an error list.
        """
        response_data = self.__organization_client.export_request_data(
            assistant_name=assistant_name,
            status=status,
            skip=skip,
            count=count
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = OrganizationResponseMapper.map_to_item_list_response(response_data)

        return result
