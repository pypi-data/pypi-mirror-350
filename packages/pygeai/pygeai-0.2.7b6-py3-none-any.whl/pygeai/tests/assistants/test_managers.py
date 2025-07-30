from unittest import TestCase
from unittest.mock import patch

from pygeai.assistant.managers import AssistantManager
from pygeai.core.models import Assistant, LlmSettings, WelcomeData, TextAssistant, ChatAssistant
from pygeai.core.base.session import get_session
from pygeai.core.responses import NewAssistantResponse

session = get_session()


class TestAssistantManager(TestCase):
    """
    python -m unittest pygeai.tests.assistants.test_managers.TestAssistantManager
    """

    def setUp(self):
        self.manager = AssistantManager()

    @patch("pygeai.assistant.clients.AssistantClient.get_assistant_data")
    def test_get_assistant_data_mocked(self, mock_get_assistant_data):
        """Test get_assistant_data with a mocked API response."""
        mock_get_assistant_data.return_value = {
            "assistantId": "123",
            "assistantName": "Test Assistant"
        }
        result = self.manager.get_assistant_data(assistant_id="123")
        self.assertIsInstance(result, Assistant)

    @patch("pygeai.assistant.clients.AssistantClient.create_assistant")
    def test_create_text_assistant_mocked(self, mock_create_assistant):
        """Test create_text_assistant with a mocked API response."""
        mock_create_assistant.return_value = {"projectId": "123", "projectName": "Test Project"}

        llm_settings = LlmSettings(provider_name="openai", model_name="GPT-4", temperature=0.7)
        welcome_data = WelcomeData(title="Welcome!", description="Welcome to the assistant")
        assistant = TextAssistant(
            name="Text Assistant",
            prompt="Prompt",
            description="Description",
            llm_settings=llm_settings,
            welcome_data=welcome_data
        )

        response = self.manager.create_assistant(assistant)
        self.assertIsInstance(response, NewAssistantResponse)

    @patch("pygeai.assistant.clients.AssistantClient.create_assistant")
    def test_create_chat_assistant_mocked(self, mock_create_assistant):
        """Test create_chat_assistant with a mocked API response."""
        mock_create_assistant.return_value = {"projectId": "456", "projectName": "Test Project"}

        llm_settings = LlmSettings(provider_name="openai", model_name="GPT-4", temperature=0.8)
        welcome_data = WelcomeData(title="Hello!", description="Welcome to the assistant")
        assistant = ChatAssistant(
            name="Chat Assistant",
            prompt="Chat Prompt",
            description="Description",
            llm_settings=llm_settings,
            welcome_data=welcome_data
        )

        response = self.manager.create_assistant(assistant)
        self.assertIsInstance(response, NewAssistantResponse)
