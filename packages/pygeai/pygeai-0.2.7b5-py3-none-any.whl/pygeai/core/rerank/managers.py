from pygeai.core.base.mappers import ErrorMapper
from pygeai.core.handlers import ErrorHandler
from pygeai.core.rerank.clients import RerankClient
from pygeai.core.rerank.mappers import RerankResponseMapper
from pygeai.core.rerank.models import RerankResponse


class RerankManager:

    def __init__(self, api_key: str = None, base_url: str = None, alias: str = "default"):
        self.__client = RerankClient(api_key, base_url, alias)

    def rerank_chunks(
            self,
            query: str,
            model: str,
            documents: list[str],
            top_n: int = 3
    ) -> RerankResponse:
        response_data = self.__client.rerank_chunks(
            query=query,
            model=model,
            documents=documents,
            top_n=top_n
        )
        if ErrorHandler.has_errors(response_data):
            result = ErrorHandler.extract_error(response_data)
        else:
            result = RerankResponseMapper.map_to_rerank_response(response_data)
        return result
