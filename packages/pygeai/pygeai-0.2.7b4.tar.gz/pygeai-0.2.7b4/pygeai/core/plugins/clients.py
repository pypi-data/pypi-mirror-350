from json import JSONDecodeError
from typing import Optional, List, Dict

from pygeai.core.base.clients import BaseClient
from pygeai.core.plugins.endpoints import LIST_ASSISTANTS_PLUGINS_V1


class PluginClient(BaseClient):
    """
    Client for interacting with plugin endpoints of the API.
    """

    def list_assistants(
        self,
        organization_id: str,
        project_id: str
    ) -> dict:
        params = {
            "organization": organization_id,
            "project": project_id,
        }

        response = self.api_service.get(
            endpoint=LIST_ASSISTANTS_PLUGINS_V1,
            params=params
        )
        try:
            result = response.json()
        except JSONDecodeError:
            result = response.text

        return result
