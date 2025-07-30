from unittest import TestCase
from unittest.mock import patch

from pygeai.assistant.managers import AssistantManager
from pygeai.assistant.rag.models import RAGAssistant, Document, UploadDocument, SearchOptions, Search, RetrieverOptions, \
    EmbeddingsOptions
from pygeai.assistant.rag.responses import DocumentListResponse
from pygeai.core.base.responses import EmptyResponse
from pygeai.core.common.exceptions import MissingRequirementException
from pygeai.core.feedback.models import FeedbackRequest
from pygeai.core.models import Assistant, LlmSettings, WelcomeData, TextAssistant, ChatAssistant, ChatWithDataAssistant, \
    ChatMessageList, ChatMessage, AssistantRevision, ChatVariableList, ChatVariable, ToolChoice, ChatToolList, \
    ToolChoiceObject, ToolChoiceFunction, ChatTool
from pygeai.core.base.session import get_session
from pygeai.core.responses import NewAssistantResponse, ChatResponse, ProviderResponse

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

    def test_get_assistant_data_no_id_or_name(self):
        """Test get_assistant_data raises MissingRequirementException when neither ID nor name is provided."""
        with self.assertRaises(MissingRequirementException):
            self.manager.get_assistant_data()

    @patch("pygeai.assistant.rag.clients.RAGAssistantClient.get_assistant_data")
    def test_get_assistant_data_by_name_mocked(self, mock_get_assistant_data):
        """Test _get_assistant_data_by_name with a mocked API response."""
        mock_get_assistant_data.return_value = {
            "name": "RAG Assistant",
            "description": "RAG Description",
            "searchOptions": {
                "historyCount": 10,
                "llm": {"providerName": "openai", "modelName": "gpt-4", "temperature": 0.7},
                "search": {
                    "k": 5,
                    "type": "similarity",
                    "prompt": "Search prompt",
                    "returnSourceDocuments": True,
                    "scoreThreshold": 0.5,
                    "template": "Search template"
                },
                "retriever": {"type": "vectorStore", "step": "all"},
                "embeddings": {
                    "dimensions": 1536,
                    "modelName": "text-embedding-ada-002",
                    "provider": "openai",
                    "useProxy": False
                }
            },
            "llmSettings": {"modelName": "gpt-4", "temperature": 0.7}
        }
        result = self.manager._get_assistant_data_by_name(assistant_name="RAG Assistant")
        self.assertIsInstance(result, RAGAssistant)

    @patch("pygeai.assistant.clients.AssistantClient.get_assistant_data")
    def test_get_assistant_data_by_id_error(self, mock_get_assistant_data):
        """Test _get_assistant_data_by_id with an error response."""
        mock_get_assistant_data.return_value = {"errors": [{"message": "Not found"}]}
        result = self.manager._get_assistant_data_by_id(assistant_id="123")
        self.assertTrue(hasattr(result, "errors"))

    @patch("pygeai.assistant.rag.clients.RAGAssistantClient.create_assistant")
    def test_create_rag_assistant_mocked(self, mock_create_assistant):
        """Test _create_rag_assistant with a mocked API response."""
        mock_create_assistant.return_value = {
            "name": "RAG Assistant",
            "description": "RAG Description",
            "searchOptions": {
                "historyCount": 10,
                "llm": {"providerName": "openai", "modelName": "gpt-4", "temperature": 0.7},
                "search": {
                    "k": 5,
                    "type": "similarity",
                    "prompt": "Search prompt",
                    "returnSourceDocuments": True,
                    "scoreThreshold": 0.5,
                    "template": "Search template"
                },
                "retriever": {"type": "vectorStore", "step": "all"},
                "embeddings": {
                    "dimensions": 1536,
                    "modelName": "text-embedding-ada-002",
                    "provider": "openai",
                    "useProxy": False
                }
            },
            "llmSettings": {"modelName": "gpt-4", "temperature": 0.7}
        }
        assistant = RAGAssistant(
            name="RAG Assistant",
            description="RAG Description",
            search_options=SearchOptions(
                history_count=10,
                llm=LlmSettings(provider_name="openai", model_name="gpt-4", temperature=0.7),
                search=Search(
                    k=5,
                    type="similarity",
                    prompt="Search prompt",
                    return_source_documents=True,
                    score_threshold=0.5,
                    template="Search template"
                ),
                retriever=RetrieverOptions(type="vectorStore", step="all"),
                embeddings=EmbeddingsOptions(
                    dimensions=1536,
                    model_name="text-embedding-ada-002",
                    provider="openai",
                    use_proxy=False
                )
            )
        )
        response = self.manager._create_rag_assistant(assistant)
        self.assertIsInstance(response, RAGAssistant)

    @patch("pygeai.assistant.clients.AssistantClient.create_assistant")
    def test_create_chat_with_data_assistant_mocked(self, mock_create_assistant):
        """Test _create_chat_with_data_assistant with a mocked API response."""
        mock_create_assistant.return_value = {"projectId": "789", "projectName": "Test Project"}
        llm_settings = LlmSettings(provider_name="openai", model_name="GPT-4", temperature=0.9)
        welcome_data = WelcomeData(title="Data Chat!", description="Welcome to data chat")
        assistant = ChatWithDataAssistant(
            name="Data Chat Assistant",
            prompt="Data Prompt",
            description="Description",
            llm_settings=llm_settings,
            welcome_data=welcome_data
        )
        response = self.manager._create_chat_with_data_assistant(assistant)
        self.assertIsInstance(response, NewAssistantResponse)

    @patch("pygeai.assistant.clients.AssistantClient.update_assistant")
    def test_update_chat_assistant_mocked(self, mock_update_assistant):
        """Test _update_chat_assistant with a mocked API response."""
        mock_update_assistant.return_value = {"projectId": "123", "projectName": "Updated Project"}
        llm_settings = LlmSettings(provider_name="openai", model_name="GPT-4", temperature=0.7)
        welcome_data = WelcomeData(title="Updated Welcome!", description="Updated assistant")
        assistant = TextAssistant(
            id="123",
            name="Text Assistant",
            prompt="Updated Prompt",
            description="Updated Description",
            llm_settings=llm_settings,
            welcome_data=welcome_data
        )
        response = self.manager._update_chat_assistant(assistant, action="saveNewRevision")
        self.assertIsInstance(response, NewAssistantResponse)

    def test_update_chat_assistant_invalid_action(self):
        """Test _update_chat_assistant with an invalid action."""
        assistant = TextAssistant(id="123", name="Test Assistant", prompt="Prompt")
        with self.assertRaises(ValueError):
            self.manager._update_chat_assistant(assistant, action="invalid_action")

    def test_update_chat_assistant_missing_revision_id(self):
        """Test _update_chat_assistant with action 'save' and no revision_id."""
        assistant = TextAssistant(id="123", name="Test Assistant", prompt="Prompt")
        with self.assertRaises(MissingRequirementException):
            self.manager._update_chat_assistant(assistant, action="save")

    @patch("pygeai.assistant.rag.clients.RAGAssistantClient.update_assistant")
    def test_update_rag_assistant_mocked(self, mock_update_assistant):
        """Test _update_rag_assistant with a mocked API response."""
        mock_update_assistant.return_value = {
            "name": "RAG Assistant",
            "description": "Updated RAG Description",
            "searchOptions": {
                "historyCount": 10,
                "llm": {"providerName": "openai", "modelName": "gpt-4", "temperature": 0.7},
                "search": {
                    "k": 5,
                    "type": "similarity",
                    "prompt": "Search prompt",
                    "returnSourceDocuments": True,
                    "scoreThreshold": 0.5,
                    "template": "Search template"
                },
                "retriever": {"type": "vectorStore", "step": "all"},
                "embeddings": {
                    "dimensions": 1536,
                    "modelName": "text-embedding-ada-002",
                    "provider": "openai",
                    "useProxy": False
                }
            },
            "llmSettings": {"modelName": "gpt-4", "temperature": 0.7}
        }
        assistant = RAGAssistant(
            name="RAG Assistant",
            description="Updated RAG Description",
            search_options=SearchOptions(
                history_count=10,
                llm=LlmSettings(provider_name="openai", model_name="gpt-4", temperature=0.7),
                search=Search(
                    k=5,
                    type="similarity",
                    prompt="Search prompt",
                    return_source_documents=True,
                    score_threshold=0.5,
                    template="Search template"
                ),
                retriever=RetrieverOptions(type="vectorStore", step="all"),
                embeddings=EmbeddingsOptions(
                    dimensions=1536,
                    model_name="text-embedding-ada-002",
                    provider="openai",
                    use_proxy=False
                )
            )
        )
        response = self.manager._update_rag_assistant(assistant)
        self.assertIsInstance(response, RAGAssistant)

    @patch("pygeai.assistant.clients.AssistantClient.delete_assistant")
    def test_delete_assistant_by_id_mocked(self, mock_delete_assistant):
        """Test _delete_assistant_by_id with a mocked API response."""
        mock_delete_assistant.return_value = {}
        response = self.manager._delete_assistant_by_id(assistant_id="123")
        self.assertIsInstance(response, EmptyResponse)

    @patch("pygeai.assistant.rag.clients.RAGAssistantClient.delete_assistant")
    def test_delete_assistant_by_name_mocked(self, mock_delete_assistant):
        """Test _delete_assistant_by_name with a mocked API response."""
        mock_delete_assistant.return_value = {}
        response = self.manager._delete_assistant_by_name(assistant_name="RAG Assistant")
        self.assertIsInstance(response, EmptyResponse)

    def test_delete_assistant_no_id_or_name(self):
        """Test delete_assistant raises MissingRequirementException when neither ID nor name is provided."""
        with self.assertRaises(MissingRequirementException):
            self.manager.delete_assistant()

    @patch("pygeai.assistant.clients.AssistantClient.send_chat_request")
    def test_send_chat_request_mocked(self, mock_send_chat_request):
        """Test send_chat_request with a mocked API response."""
        mock_send_chat_request.return_value = {"response": "Chat response"}
        assistant = TextAssistant(id="123", name="Test Assistant", prompt="Prompt")
        messages = ChatMessageList(messages=[ChatMessage(role="user", content="Hello")])
        response = self.manager.send_chat_request(assistant, messages)
        self.assertIsInstance(response, ChatResponse)

    @patch("pygeai.assistant.clients.AssistantClient.get_request_status")
    def test_get_request_status_mocked(self, mock_get_request_status):
        """Test get_request_status with a mocked API response."""
        mock_get_request_status.return_value = {"status": "completed"}
        response = self.manager.get_request_status(request_id="req123")
        self.assertIsInstance(response, ChatResponse)

    @patch("pygeai.assistant.clients.AssistantClient.cancel_request")
    def test_cancel_request_mocked(self, mock_cancel_request):
        """Test cancel_request with a mocked API response."""
        mock_cancel_request.return_value = {"status": "canceled"}
        response = self.manager.cancel_request(request_id="req123")
        self.assertIsInstance(response, ChatResponse)

    @patch("pygeai.chat.clients.ChatClient.chat_completion")
    def test_chat_completion_mocked(self, mock_chat_completion):
        """Test chat_completion with a mocked API response."""
        mock_chat_completion.return_value = {
            "created": 1697059200,
            "model": "gpt-4",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            "response": "Completion response"
        }
        messages = ChatMessageList(messages=[ChatMessage(role="user", content="Hello")])
        llm_settings = LlmSettings(provider_name="openai", model_name="GPT-4", temperature=0.7)
        response = self.manager.chat_completion(
            model="GPT-4",
            messages=messages,
            llm_settings=llm_settings
        )
        self.assertIsInstance(response, ProviderResponse)

    @patch("pygeai.assistant.rag.clients.RAGAssistantClient.get_documents")
    def test_get_document_list_mocked(self, mock_get_documents):
        """Test get_document_list with a mocked API response."""
        mock_get_documents.return_value = {
            "documents": [{
                "id": "doc1",
                "name": "Document 1",
                "chunks": "chunk_data",
                "extension": "pdf",
                "indexStatus": "indexed",
                "url": "http://example.com/doc1",
                "metadata": [],
                "timestamp": "2025-05-23T16:52:00+00:00"
            }],
            "count": 1
        }
        response = self.manager.get_document_list(name="RAG Assistant")
        self.assertIsInstance(response, DocumentListResponse)

    @patch("pygeai.assistant.rag.clients.RAGAssistantClient.delete_all_documents")
    def test_delete_all_documents_mocked(self, mock_delete_all_documents):
        """Test delete_all_documents with a mocked API response."""
        mock_delete_all_documents.return_value = {}
        response = self.manager.delete_all_documents(name="RAG Assistant")
        self.assertIsInstance(response, EmptyResponse)

    @patch("pygeai.assistant.rag.clients.RAGAssistantClient.retrieve_document")
    def test_get_document_mocked(self, mock_retrieve_document):
        """Test get_document with a mocked API response."""
        mock_retrieve_document.return_value = {
            "id": "doc1",
            "name": "Document 1",
            "chunks": "chunk_data",
            "extension": "pdf",
            "indexStatus": "indexed",
            "url": "http://example.com/doc1",
            "metadata": [],
            "timestamp": "2025-05-23T16:52:00+00:00"
        }
        response = self.manager.get_document(name="RAG Assistant", document_id="doc1")
        self.assertIsInstance(response, Document)

    @patch("pygeai.assistant.rag.clients.RAGAssistantClient.upload_document")
    def test_upload_document_mocked(self, mock_upload_document):
        """Test upload_document with a mocked API response."""
        mock_upload_document.return_value = {
            "id": "doc1",
            "name": "Document 1",
            "chunks": "chunk_data",
            "extension": "pdf",
            "indexStatus": "indexed",
            "url": "http://example.com/doc1",
            "metadata": [],
            "timestamp": "2025-05-23T16:52:00+00:00"
        }
        assistant = RAGAssistant(name="RAG Assistant")
        document = UploadDocument(
            path="path/to/doc.pdf",
            upload_type="multipart",
            content_type="application/pdf"
        )
        response = self.manager.upload_document(assistant, document)
        self.assertIsInstance(response, Document)

    @patch("pygeai.assistant.rag.clients.RAGAssistantClient.delete_document")
    def test_delete_document_mocked(self, mock_delete_document):
        """Test delete_document with a mocked API response."""
        mock_delete_document.return_value = {}
        response = self.manager.delete_document(name="RAG Assistant", document_id="doc1")
        self.assertIsInstance(response, EmptyResponse)

    @patch("pygeai.core.feedback.clients.FeedbackClient.send_feedback")
    def test_send_feedback_mocked(self, mock_send_feedback):
        """Test send_feedback with a mocked API response."""
        mock_send_feedback.return_value = {}
        feedback = FeedbackRequest(
            request_id="req123",
            origin="test",
            answer_score=5,
            comments="Great response!"
        )
        response = self.manager.send_feedback(feedback)
        self.assertIsInstance(response, EmptyResponse)

    @patch("pygeai.assistant.clients.AssistantClient.get_assistant_data")
    def test_get_assistant_data_full_detail(self, mock_get_assistant_data):
        """Test get_assistant_data with full detail option."""
        mock_get_assistant_data.return_value = {
            "assistantId": "123",
            "assistantName": "Test Assistant",
            "details": "Full details"
        }
        result = self.manager.get_assistant_data(assistant_id="123", detail="full")
        self.assertIsInstance(result, Assistant)

    @patch("pygeai.assistant.clients.AssistantClient.send_chat_request")
    def test_send_chat_request_with_revision_and_variables(self, mock_send_chat_request):
        """Test send_chat_request with revision and variables."""
        mock_send_chat_request.return_value = {"response": "Chat response"}
        assistant = TextAssistant(id="123", name="Test Assistant", prompt="Prompt")
        messages = ChatMessageList(messages=[ChatMessage(role="user", content="Hello")])
        revision = AssistantRevision(revision_id=1, revision_name="Revision 1")
        variables = ChatVariableList(variables=[ChatVariable(key="var1", value="value1")])
        response = self.manager.send_chat_request(assistant, messages, revision, variables)
        self.assertIsInstance(response, ChatResponse)

    @patch("pygeai.chat.clients.ChatClient.chat_completion")
    def test_chat_completion_with_tools(self, mock_chat_completion):
        """Test chat_completion with tool choice and tools."""
        mock_chat_completion.return_value = {
            "created": 1697059200,
            "model": "gpt-4",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            "response": "Completion with tools"
        }
        messages = ChatMessageList(messages=[ChatMessage(role="user", content="Use tool")])
        llm_settings = LlmSettings(provider_name="openai", model_name="GPT-4", temperature=0.7)
        tool_choice = ToolChoice(tool_choice=ToolChoiceObject(function=ToolChoiceFunction(name="test_function")))
        tools = ChatToolList(tools=[ChatTool(name="test_function")])
        response = self.manager.chat_completion(
            model="GPT-4",
            messages=messages,
            llm_settings=llm_settings,
            tool_choice=tool_choice,
            tools=tools
        )
        self.assertIsInstance(response, ProviderResponse)

    def test_assistant_manager_init_no_api_key(self):
        """Test AssistantManager initialization with no api_key"""
        manager = AssistantManager(api_key=None, base_url="http://test.com", alias="test")
        self.assertIsInstance(manager, AssistantManager)

    @patch("pygeai.assistant.clients.AssistantClient.create_assistant")
    def test_create_assistant_invalid_input(self, mock_create_assistant):
        """Test create_assistant with invalid assistant data."""
        mock_create_assistant.return_value = {"errors": [{"message": "Invalid assistant data"}]}
        assistant = TextAssistant(name="", prompt="", description="")  # Invalid: empty name/prompt
        response = self.manager.create_assistant(assistant)
        self.assertTrue(hasattr(response, "errors"))

    @patch("pygeai.assistant.clients.AssistantClient.create_assistant")
    def test_create_assistant_server_error(self, mock_create_assistant):
        """Test create_assistant with server error."""
        mock_create_assistant.return_value = {"errors": [{"message": "Server error", "code": 500}]}
        llm_settings = LlmSettings(provider_name="openai", model_name="GPT-4", temperature=0.7)
        assistant = TextAssistant(
            name="Test Assistant",
            prompt="Prompt",
            description="Description",
            llm_settings=llm_settings
        )
        response = self.manager.create_assistant(assistant)
        self.assertTrue(hasattr(response, "errors"))

    @patch("pygeai.assistant.clients.AssistantClient.update_assistant")
    def test_update_assistant_missing_id(self, mock_update_assistant):
        """Test update_assistant with missing assistant ID."""
        mock_update_assistant.return_value = {"errors": [{"message": "Missing assistant ID"}]}
        assistant = TextAssistant(name="Test Assistant", prompt="Prompt", description="Description")
        with self.assertRaises(MissingRequirementException):
            self.manager._update_chat_assistant(assistant, action="saveNewRevision")

    @patch("pygeai.assistant.clients.AssistantClient.delete_assistant")
    def test_delete_assistant_not_found(self, mock_delete_assistant):
        """Test delete_assistant with not found error."""
        mock_delete_assistant.return_value = {"errors": [{"message": "Assistant not found", "code": 404}]}
        response = self.manager._delete_assistant_by_id(assistant_id="999")
        self.assertTrue(hasattr(response, "errors"))

    @patch("pygeai.assistant.clients.AssistantClient.send_chat_request")
    def test_send_chat_request_empty_messages(self, mock_send_chat_request):
        """Test send_chat_request with empty messages."""
        mock_send_chat_request.return_value = {"errors": [{"message": "No messages provided"}]}
        assistant = TextAssistant(id="123", name="Test Assistant", prompt="Prompt")
        messages = ChatMessageList(messages=[])
        response = self.manager.send_chat_request(assistant, messages)
        self.assertTrue(hasattr(response, "errors"))

    @patch("pygeai.assistant.clients.AssistantClient.get_request_status")
    def test_get_request_status_invalid_id(self, mock_get_request_status):
        """Test get_request_status with invalid request ID."""
        mock_get_request_status.return_value = {"errors": [{"message": "Invalid request ID", "code": 400}]}
        response = self.manager.get_request_status(request_id="invalid_id")
        self.assertTrue(hasattr(response, "errors"))

    @patch("pygeai.assistant.clients.AssistantClient.cancel_request")
    def test_cancel_request_not_found(self, mock_cancel_request):
        """Test cancel_request with not found error."""
        mock_cancel_request.return_value = {"errors": [{"message": "Request not found", "code": 404}]}
        response = self.manager.cancel_request(request_id="nonexistent_id")
        self.assertTrue(hasattr(response, "errors"))