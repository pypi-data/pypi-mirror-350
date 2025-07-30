from unittest import TestCase
from unittest.mock import patch

from pygeai.assistant.clients import AssistantClient
from pygeai.core.base.session import get_session

session = get_session()


class TestAssistantClient(TestCase):
    """
    python -m unittest pygeai.tests.assistants.test_clients.TestAssistantClient
    """

    def setUp(self):
        self.client = AssistantClient()

    @patch("pygeai.core.services.rest.ApiService.get")
    def test_get_assistant_data(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"assistant": {"id": "123", "name": "assistant1"}}

        result = self.client.get_assistant_data("123")

        self.assertIsNotNone(result)
        self.assertEqual(result['assistant']['name'], "assistant1")

    @patch("pygeai.core.services.rest.ApiService.post")
    def test_create_assistant(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.json.return_value = {"assistant": {"id": "123", "name": "assistant1"}}

        result = self.client.create_assistant(
            assistant_type="text",
            name="assistant1",
            prompt="Hello",
            description="Test assistant"
        )

        self.assertIsNotNone(result)
        self.assertEqual(result['assistant']['name'], "assistant1")

    @patch("pygeai.core.services.rest.ApiService.put")
    def test_update_assistant(self, mock_put):
        mock_response = mock_put.return_value
        mock_response.json.return_value = {"assistant": {"id": "123", "name": "updated_assistant"}}

        result = self.client.update_assistant(
            assistant_id="123",
            status=1,
            action="save",
            name="updated_assistant"
        )

        self.assertIsNotNone(result)
        self.assertEqual(result['assistant']['name'], "updated_assistant")

    @patch("pygeai.core.services.rest.ApiService.delete")
    def test_delete_assistant(self, mock_delete):
        mock_response = mock_delete.return_value
        mock_response.json.return_value = {"status": "deleted"}

        result = self.client.delete_assistant("123")

        self.assertIsNotNone(result)
        self.assertEqual(result['status'], "deleted")

    @patch("pygeai.core.services.rest.ApiService.post")
    def test_send_chat_request(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.json.return_value = {"status": "success"}

        result = self.client.send_chat_request(
            assistant_name="assistant1",
            messages=[{"role": "user", "content": "Hello"}],
            revision="1",
            revision_name="v1"
        )

        self.assertIsNotNone(result)
        self.assertEqual(result['status'], "success")

    @patch("pygeai.core.services.rest.ApiService.get")
    def test_get_request_status(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"status": "completed"}

        result = self.client.get_request_status("req123")

        self.assertIsNotNone(result)
        self.assertEqual(result['status'], "completed")

    @patch("pygeai.core.services.rest.ApiService.post")
    def test_cancel_request(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.json.return_value = {"status": "canceled"}

        result = self.client.cancel_request("req123")

        self.assertIsNotNone(result)
        self.assertEqual(result['status'], "canceled")
