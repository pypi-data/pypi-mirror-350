from pygeai.core.base.mappers import ErrorMapper, ModelMapper
from pygeai.core.models import UsageLimit
from pygeai.organization.limits.clients import UsageLimitClient


class UsageLimitManager:
    """
    Manages usage limits for an organization and its projects.

    This class provides methods to set, retrieve, update, and delete usage limits
    at both the organization and project levels. It interacts with the `UsageLimitClient`
    to perform API operations.

    Attributes:
        __client (UsageLimitClient): Client for making API requests.
        __organization_id (str): The organization ID for which usage limits are managed.
    """

    def __init__(
            self,
            api_key: str = None,
            base_url: str = None,
            alias: str = "default",
            organization_id: str = None
    ):
        self.__client = UsageLimitClient(api_key, base_url, alias)
        self.__organization_id = organization_id

    def set_organization_usage_limit(self, usage_limit: UsageLimit) -> UsageLimit:
        """
        Sets a new usage limit for the organization.

        :param usage_limit: UsageLimit object containing the limit details.
        :return: UsageLimit object with the created usage limit details.
        """
        response_data = self.__client.set_organization_usage_limit(
            organization=self.__organization_id,
            usage_limit=usage_limit.to_dict()
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ModelMapper.map_to_usage_limit(response_data)

        return result

    def get_latest_usage_limit_from_organization(self) -> UsageLimit:
        """
        Retrieves the latest usage limit set for the organization.

        :return: UsageLimit object containing the latest usage limit details.
        """
        response_data = self.__client.get_organization_latest_usage_limit(
            organization=self.__organization_id
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ModelMapper.map_to_usage_limit(response_data)

        return result

    def get_all_usage_limits_from_organization(self) -> list[UsageLimit]:
        """
        Retrieves all usage limits associated with the organization.

        :return: UsageLimit object containing all usage limits for the organization.
        """
        response_data = self.__client.get_all_usage_limits_from_organization(
            organization=self.__organization_id
        )
        
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ModelMapper.map_to_usage_limit_list(response_data)

        return result

    def update_organization_usage_limit(self, usage_limit: UsageLimit) -> UsageLimit:
        """
        Updates the usage limits for an organization, including hard limit, soft limit, and renewal status.

        :param usage_limit: UsageLimit object containing the updated limit values.
        :return: UsageLimit object with updated usage limit details.
        """
        response_data = {}
        if usage_limit.hard_limit:
            response_data = self.__client.set_organization_hard_limit(
                organization=self.__organization_id,
                limit_id=usage_limit.id,
                hard_limit=usage_limit.hard_limit
            )
        if usage_limit.soft_limit:
            response_data = self.__client.set_organization_soft_limit(
                organization=self.__organization_id,
                limit_id=usage_limit.id,
                soft_limit=usage_limit.soft_limit
            )
        if usage_limit.renewal_status:
            response_data = self.__client.set_organization_renewal_status(
                organization=self.__organization_id,
                limit_id=usage_limit.id,
                renewal_status=usage_limit.renewal_status
            )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ModelMapper.map_to_usage_limit(response_data)

        return result

    def delete_usage_limit_from_organization(self, limit_id: str) -> UsageLimit:
        """
        Deletes a usage limit from the organization.

        :param limit_id: The ID of the usage limit to be deleted.
        :return: UsageLimit object representing the deleted limit details.
        """
        response_data = self.__client.delete_usage_limit_from_organization(
            organization=self.__organization_id,
            limit_id=limit_id,
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ModelMapper.map_to_usage_limit(response_data)

        return result

    def set_project_usage_limit(self, project_id: str, usage_limit: UsageLimit) -> UsageLimit:
        """
        Sets a new usage limit for a specific project within the organization.

        :param project_id: The unique identifier of the project.
        :param usage_limit: UsageLimit object containing the limit details.
        :return: UsageLimit object with the created project usage limit details.
        """
        response_data = self.__client.set_project_usage_limit(
            organization=self.__organization_id,
            project=project_id,
            usage_limit=usage_limit.to_dict()
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ModelMapper.map_to_usage_limit(response_data)

        return result

    def get_all_usage_limits_from_project(self, project_id: str) -> UsageLimit:
        """
        Retrieves all usage limits associated with a specific project.

        :param project_id: The unique identifier of the project.
        :return: UsageLimit object containing all usage limits for the project.
        """
        response_data = self.__client.get_all_usage_limits_from_project(
            organization=self.__organization_id,
            project=project_id,
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ModelMapper.map_to_usage_limit(response_data)

        return result

    def get_latest_usage_limit_from_project(self, project_id: str) -> UsageLimit:
        """
        Retrieves the latest usage limit set for a specific project.

        :param project_id: The unique identifier of the project.
        :return: UsageLimit object containing the latest usage limit details.
        """
        response_data = self.__client.get_latest_usage_limit_from_project(
            organization=self.__organization_id,
            project=project_id,
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ModelMapper.map_to_usage_limit(response_data)

        return result

    def get_active_usage_limit_from_project(self, project_id: str) -> UsageLimit:
        """
        Retrieves the currently active usage limit for a specific project.

        :param project_id: The unique identifier of the project.
        :return: UsageLimit object containing the active usage limit details.
        """
        response_data = self.__client.get_active_usage_limit_from_project(
            organization=self.__organization_id,
            project=project_id,
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ModelMapper.map_to_usage_limit(response_data)

        return result

    def delete_usage_limit_from_project(self, project_id: str, usage_limit: UsageLimit) -> UsageLimit:
        """
        Deletes a specified usage limit from a project.

        :param project_id: The unique identifier of the project.
        :param usage_limit: The UsageLimit object representing the limit to be deleted.
        :return: UsageLimit object representing the deleted usage limit details.
        """
        response_data = self.__client.delete_usage_limit_from_project(
            organization=self.__organization_id,
            project=project_id,
            limit_id=usage_limit.id
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ModelMapper.map_to_usage_limit(response_data)

        return result

    def update_project_usage_limit(self, project_id: str, usage_limit: UsageLimit) -> UsageLimit:
        """
        Updates the usage limits for a specific project, including hard limit, soft limit, and renewal status.

        :param project_id: The unique identifier of the project.
        :param usage_limit: UsageLimit object containing the updated limit values.
        :return: UsageLimit object with updated usage limit details.
        """
        response_data = {}
        if usage_limit.hard_limit:
            response_data = self.__client.set_hard_limit_for_active_usage_limit_from_project(
                organization=self.__organization_id,
                project=project_id,
                limit_id=usage_limit.id,
                hard_limit=usage_limit.hard_limit
            )
        if usage_limit.soft_limit:
            response_data = self.__client.set_soft_limit_for_active_usage_limit_from_project(
                organization=self.__organization_id,
                project=project_id,
                limit_id=usage_limit.id,
                soft_limit=usage_limit.soft_limit
            )
        if usage_limit.renewal_status:
            response_data = self.__client.set_project_renewal_status(
                organization=self.__organization_id,
                project=project_id,
                limit_id=usage_limit.id,
                renewal_status=usage_limit.renewal_status
            )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ModelMapper.map_to_usage_limit(response_data)

        return result


