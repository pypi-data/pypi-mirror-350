from spryx_core import NOT_GIVEN, is_given
from spryx_http import SpryxAsyncClient


class Credentials:
    def __init__(self, client: SpryxAsyncClient):
        self._client = client

    async def list_credentials(
        self,
        page: int = 1,
        limit: int = 10,
        order: str = "asc",
        type: str = NOT_GIVEN,
    ) -> dict:
        """List all credentials."""
        params = {"page": page, "limit": limit, "order": order}
        
        if is_given(type):
            params["type"] = type
            
        return await self._client.get(
            "/v1/credentials/",
            params=params,
        )

    async def create_credential(
        self,
        title: str,
        type: str,
        values: dict,
    ) -> dict:
        """Create a new credential."""
        payload = {
            "title": title,
            "type": type,
            "values": values,
        }

        return await self._client.post("/v1/credentials/", json=payload)

    async def get_credential(
        self,
        credential_id: str,
    ) -> dict:
        """Retrieve a credential by ID."""
        return await self._client.get(f"/v1/credentials/{credential_id}")

    async def update_credential(
        self,
        credential_id: str,
        title: str = NOT_GIVEN,
        values: dict = NOT_GIVEN,
    ) -> dict:
        """Update an existing credential."""
        payload = {}
        
        if is_given(title):
            payload["title"] = title
            
        if is_given(values):
            payload["values"] = values

        return await self._client.put(
            f"/v1/credentials/{credential_id}",
            json=payload,
        )

    async def delete_credential(
        self,
        credential_id: str,
    ) -> dict:
        """Delete a credential."""
        return await self._client.delete(f"/v1/credentials/{credential_id}") 