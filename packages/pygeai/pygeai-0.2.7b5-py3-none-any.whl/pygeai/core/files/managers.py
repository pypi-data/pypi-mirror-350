from pygeai.core.base.mappers import ErrorMapper, ResponseMapper
from pygeai.core.base.responses import EmptyResponse
from pygeai.core.files.clients import FileClient
from pygeai.core.files.models import UploadFile, File, FileList
from pygeai.core.files.mappers import FileResponseMapper
from pygeai.core.files.responses import UploadFileResponse
from pygeai.core.handlers import ErrorHandler


class FileManager:
    """
    Manages file-related operations such as uploading, retrieving, and deleting files
    within an organization and project.
    """

    def __init__(
            self,
            api_key: str = None,
            base_url: str = None,
            alias: str = "default",
            organization_id: str = None,
            project_id: str = None
    ):
        self.__client = FileClient(
            api_key,
            base_url,
            alias
        )
        self.__organization_id = organization_id
        self.__project_id = project_id

    def upload_file(
            self,
            file: UploadFile
    ) -> UploadFileResponse:
        """
        Uploads a file to the specified organization and project.

        :param file: UploadFile - The file object containing file path, name, and folder details.
        :return: UploadFileResponse - The response object containing the uploaded file details.
        """
        response_data = self.__client.upload_file(
            file_path=file.path,
            organization_id=self.__organization_id,
            project_id=self.__project_id,
            folder=file.folder,
            file_name=file.name,
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = FileResponseMapper.map_to_upload_file_response(response_data)
        return result

    def get_file_data(
            self,
            file_id: str
    ) -> File:
        """
        Retrieves metadata of a specific file by its ID.

        :param file_id: str - The unique identifier of the file.
        :return: File - A file object containing metadata about the requested file.
        """
        response_data = self.__client.get_file(
            organization=self.__organization_id,
            project=self.__project_id,
            file_id=file_id
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = FileResponseMapper.map_to_file(response_data)
        return result

    def delete_file(
            self,
            file_id: str
    ) -> EmptyResponse:
        """
        Deletes a file from the specified organization and project.

        :param file_id: str - The unique identifier of the file to be deleted.
        :return: EmptyResponse - Response indicating the success or failure of the operation.
        """
        response_data = self.__client.delete_file(
            organization=self.__organization_id,
            project=self.__project_id,
            file_id=file_id
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = ResponseMapper.map_to_empty_response(response_data)
        return result

    def get_file_content(
            self,
            file_id: str
    ) -> bytes:
        """
        Retrieves the raw content of a specific file.

        :param file_id: str - The unique identifier of the file.
        :return: bytes - The binary content of the file.
        """
        response_data = self.__client.get_file_content(
            organization=self.__organization_id,
            project=self.__project_id,
            file_id=file_id
        )
        if isinstance(response_data, dict) and "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = response_data
        return result

    def get_file_list(self) -> FileList:
        """
         Retrieves a list of all files associated with a given organization and project.

        :return: FileList - A list of file objects associated with the organization and project.
        """
        response_data = self.__client.get_file_list(
            organization=self.__organization_id,
            project=self.__project_id
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = FileResponseMapper.map_to_file_list_response(response_data)
        return result

