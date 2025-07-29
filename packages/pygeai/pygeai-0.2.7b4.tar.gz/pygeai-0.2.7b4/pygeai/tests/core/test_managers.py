import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

from pygeai.core.base.mappers import ResponseMapper
from pygeai.core.models import Project
from pygeai.core.base.responses import EmptyResponse, ErrorListResponse
from pygeai.organization.managers import OrganizationManager
from pygeai.organization.clients import OrganizationClient
from pygeai.organization.mappers import OrganizationResponseMapper
from pygeai.organization.responses import AssistantListResponse, ProjectListResponse, ProjectDataResponse, \
    ProjectTokensResponse, ProjectItemListResponse


class TestGeai(TestCase):
    """
    python -m unittest pygeai.tests.core.test_managers.TestGeai
    """

    def setUp(self):
        self.manager = OrganizationManager()
        self.mock_client = MagicMock(spec=OrganizationClient)
        with patch("pygeai.organization.clients.OrganizationClient", return_value=self.mock_client):
            self.geai = OrganizationManager(api_key="test_key", base_url="http://test.url")

    def test_get_assistant_list(self):
        mock_response = AssistantListResponse(assistants=[])

        with patch.object(self.geai._OrganizationManager__organization_client, 'get_assistant_list', return_value={}):
            with patch.object(OrganizationResponseMapper, 'map_to_assistant_list_response', return_value=mock_response):
                response = self.geai.get_assistant_list()

        self.assertIsInstance(response, AssistantListResponse)
        self.assertEqual(response.assistants, [])

    def test_get_project_list(self):
        mock_response = ProjectListResponse(projects=[])

        with patch.object(self.geai._OrganizationManager__organization_client, 'get_project_list', return_value={}):
            with patch.object(OrganizationResponseMapper, 'map_to_project_list_response', return_value=mock_response):
                response = self.geai.get_project_list()

        self.assertIsInstance(response, ProjectListResponse)
        self.assertEqual(response.projects, [])

    def test_get_project_data(self):
        mock_project = Project(
            id="123",
            name="Test Project",
            description="Test Description",
            email="test@example.com",
            usage_limit=None
        )

        mock_response = ProjectDataResponse(project=mock_project)

        with patch.object(self.geai._OrganizationManager__organization_client, 'get_project_data', return_value={}):
            with patch.object(OrganizationResponseMapper, 'map_to_project_data', return_value=mock_response):
                response = self.geai.get_project_data("123")

        self.assertIsInstance(response, ProjectDataResponse)
        self.assertEqual(response.project.name, "Test Project")

    def test_create_project(self):
        mock_project = Project(
            id="123",
            name="New Project",
            description="A test project",
            email="test@example.com",
            usage_limit=None
        )

        mock_response = ProjectDataResponse(project=mock_project)

        with patch.object(self.geai._OrganizationManager__organization_client, 'create_project', return_value={}):
            with patch.object(OrganizationResponseMapper, 'map_to_project_data', return_value=mock_response):
                response = self.geai.create_project(mock_project)

        self.assertIsInstance(response, ProjectDataResponse)
        self.assertEqual(response.project.name, "New Project")

    def test_update_project(self):
        mock_project = Project(
            id="123",
            name="Updated Project",
            description="An updated test project",
            email="test@example.com",
            usage_limit=None
        )

        mock_response = ProjectDataResponse(project=mock_project)

        with patch.object(self.geai._OrganizationManager__organization_client, 'update_project', return_value={}):
            with patch.object(OrganizationResponseMapper, 'map_to_project_data', return_value=mock_response):
                response = self.geai.update_project(mock_project)

        self.assertIsInstance(response, ProjectDataResponse)
        self.assertEqual(response.project.name, "Updated Project")

    def test_delete_project(self):
        mock_response = EmptyResponse(content={})

        with patch.object(self.geai._OrganizationManager__organization_client, 'delete_project', return_value={}):
            with patch.object(ResponseMapper, 'map_to_empty_response', return_value=mock_response):
                response = self.geai.delete_project("123")

        self.assertIsInstance(response, EmptyResponse)
        self.assertEqual(response.content, {})

    def test_get_project_tokens(self):
        mock_response = ProjectTokensResponse(tokens=[])

        with patch.object(self.geai._OrganizationManager__organization_client, 'get_project_tokens', return_value={"tokens": []}):
            with patch.object( OrganizationResponseMapper, 'map_to_token_list_response', return_value=mock_response):
                response = self.geai.get_project_tokens("123")

        self.assertIsInstance(response, ProjectTokensResponse)
        self.assertEqual(response.tokens, [])

    def test_export_request_data(self):
        mock_response = MagicMock()
        mock_response.content = '{"items": []}'

        self.mock_client.export_request_data.return_value = mock_response

        with patch.object(self.geai._OrganizationManager__organization_client, 'export_request_data', return_value={"items": []}):
            with patch.object(OrganizationResponseMapper, 'map_to_item_list_response', return_value=ProjectItemListResponse(items=[])):
                response = self.geai.export_request_data()

        self.assertIsInstance(response, ProjectItemListResponse)
        self.assertEqual(response.items, [])

    @unittest.skip("Requires call to API")
    def test_create_project_simple(self):
        project = Project(
            project_name="Test project - SDK",
            project_email="alejandro.trinidad@globant.com",
            project_description="Test project to validate programmatic creation of project"
        )
        response = self.manager.create_project(project)
        self.assertIsNotNone(response)

    @patch("pygeai.organization.clients.OrganizationClient.get_assistant_list")
    def test_get_assistant_list_mocked(self, mock_get_assistant_list):
        """Test get_assistant_list with a mocked API response."""
        mock_get_assistant_list.return_value = {
            "assistants": [
                {
                    "assistantName": "Test assistant 1",
                },
                {
                    "assistantName": "Test assistant 2",
                },
            ],
            'projectId': 'proj-123',
            'projectName': "Test Project"
        }
        result = self.manager.get_assistant_list()
        self.assertIsInstance(result, AssistantListResponse)

    @patch("pygeai.organization.clients.OrganizationClient.get_project_list")
    def test_get_project_list_mocked(self, mock_get_project_list):
        """Test get_project_list with a mocked API response."""
        mock_get_project_list.return_value = {"projects": []}
        result = self.manager.get_project_list()
        self.assertIsInstance(result, ProjectListResponse)

    @patch("pygeai.organization.clients.OrganizationClient.get_project_data")
    def test_get_project_data_mocked(self, mock_get_project_data):
        """Test get_project_data with a mocked API response."""
        mock_get_project_data.return_value = {"projectId": "123", "projectName": "Test Project"}
        result = self.manager.get_project_data("123")
        self.assertIsInstance(result, ProjectDataResponse)

    @patch("pygeai.organization.clients.OrganizationClient.create_project")
    def test_create_project_mocked(self, mock_create_project):
        """Test create_project with a mocked API response."""
        mock_create_project.return_value = {"projectId": "123", "projectName": "Test Project"}
        project = Project(name="Test Project", email="test@example.com", description="Description")
        response = self.manager.create_project(project)
        self.assertIsInstance(response, ProjectDataResponse)

    @patch("pygeai.organization.clients.OrganizationClient.update_project")
    def test_update_project_mocked(self, mock_update_project):
        """Test update_project with a mocked API response."""
        mock_update_project.return_value = {"projectId": "123", "projectName": "Updated Project"}
        project = Project(name="Updated Project", email="test@example.com", description="Updated description")
        response = self.manager.update_project(project)
        self.assertIsInstance(response, ProjectDataResponse)

    @patch("pygeai.organization.clients.OrganizationClient.delete_project")
    def test_delete_project_mocked(self, mock_delete_project):
        """Test delete_project with a mocked API response."""
        mock_delete_project.return_value = {}
        response = self.manager.delete_project("123")
        self.assertIsInstance(response, EmptyResponse)

    @patch("pygeai.organization.clients.OrganizationClient.get_project_tokens")
    def test_get_project_tokens_mocked(self, mock_get_project_tokens):
        """Test get_project_tokens with a mocked API response."""
        mock_get_project_tokens.return_value = {"tokens": []}
        result = self.manager.get_project_tokens("123")
        self.assertIsInstance(result, ProjectTokensResponse)

    @patch("pygeai.organization.clients.OrganizationClient.export_request_data")
    def test_export_request_data_mocked(self, mock_export_request_data):
        """Test export_request_data with a mocked API response."""
        mock_export_request_data.return_value = {"items": []}
        result = self.manager.export_request_data()
        self.assertIsInstance(result, ProjectItemListResponse)

    @patch("pygeai.organization.clients.OrganizationClient.get_project_data")
    def test_get_project_data_error_handling(self, mock_get_project_data):
        mock_get_project_data.return_value = {"errors": [{"id": 404, "description": "Project not found"}]}
        response = self.manager.get_project_data("invalid_id")
        self.assertTrue(isinstance(response, ErrorListResponse))
        self.assertTrue(hasattr(response, "errors"))
        error = response.errors[0]
        self.assertEqual(error.id, 404)
        self.assertEqual(error.description, "Project not found")
        self.assertEqual(str(error), "{'id': 404, 'description': 'Project not found'}")

    @patch("pygeai.organization.clients.OrganizationClient.delete_project")
    def test_delete_project_error_handling(self, mock_delete_project):
        mock_delete_project.return_value = {"errors": [{"id": 403, "description": "Permission denied"}]}
        response = self.manager.delete_project("invalid_id")
        self.assertTrue(isinstance(response, ErrorListResponse))
        self.assertTrue(hasattr(response, "errors"))
        error = response.errors[0]
        self.assertEqual(error.id, 403)
        self.assertEqual(error.description, "Permission denied")
        self.assertEqual(str(error), "{'id': 403, 'description': 'Permission denied'}")

