from spryx_core import NOT_GIVEN, is_given
from spryx_http import SpryxAsyncClient


class CredentialTypes:
    def __init__(self, client: SpryxAsyncClient):
        self._client = client

    async def list_credential_types(
        self,
        type_name: str = NOT_GIVEN,
    ) -> dict:
        """List all credential types."""
        params = {}
        
        if is_given(type_name):
            params["type_name"] = type_name
            
        return await self._client.get(
            "/credential-types/",
            params=params,
        ) 