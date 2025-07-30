import unittest
from unittest.mock import MagicMock

from pygeai.core.base.mappers import ErrorMapper
from pygeai.core.base.responses import EmptyResponse, ErrorListResponse
from pygeai.core.rerank.managers import RerankManager
from pygeai.core.rerank.mappers import RerankResponseMapper
from pygeai.core.rerank.models import RerankResponse, RerankResult, RerankMetaData


class TestRerankManager(unittest.TestCase):
    """
    python -m unittest pygeai.tests.core.rerank.test_managers.TestRerankManager
    """

    def setUp(self):
        self.manager = RerankManager()

        self.manager._RerankManager__client = MagicMock()

    def test_rerank_chunks_success(self):
        mock_response = {
            "id": "00a3bfe3-67e6-4aab-a19a-592bda2920a7",
            "results": [
                {"index": 2, "relevance_score": 0.8963332},
                {"index": 0, "relevance_score": 0.17393301},
                {"index": 1, "relevance_score": 0.08103136}
            ],
            "meta": {
                "api_version": {"version": "2"},
                "billed_units": {"search_units": 1}
            }
        }

        self.manager._RerankManager__client.rerank_chunks.return_value = mock_response

        result = self.manager.rerank_chunks(
            query="What is the Capital of the United States?",
            model="cohere/rerank-v3.5",
            documents=[
                "Carson City is the capital city of the American state of Nevada.",
                "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",
                "Washington, D.C. is the capital of the United States.",
                "Capital punishment has existed in the United States since before it was a country."
            ],
            top_n=3
        )

        self.assertIsInstance(result, RerankResponse)
        self.assertEqual(result.id, "00a3bfe3-67e6-4aab-a19a-592bda2920a7")
        self.assertEqual(len(result.results), 3)
        self.assertEqual(result.results[0].index, 2)
        self.assertEqual(result.results[0].relevance_score, 0.8963332)

    def test_rerank_chunks_error_response(self):
        mock_error_response = {
            "errors": [
                {"id": 1001, "description": "Invalid request"},
                {"id": 1002, "description": "Model not found"}
            ]
        }

        self.manager._RerankManager__client.rerank_chunks.return_value = mock_error_response

        result = self.manager.rerank_chunks(
            query="Invalid query",
            model="invalid/model",
            documents=["This should fail"],
            top_n=3
        )

        self.assertIsInstance(result, ErrorListResponse)
        self.assertEqual(len(result.errors), 2)
        self.assertEqual(result.errors[0].id, 1001)
        self.assertEqual(result.errors[0].description, "Invalid request")
        self.assertEqual(result.errors[1].id, 1002)
        self.assertEqual(result.errors[1].description, "Model not found")