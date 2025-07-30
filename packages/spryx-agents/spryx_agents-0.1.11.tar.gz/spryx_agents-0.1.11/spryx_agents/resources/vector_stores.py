from spryx_core import NOT_GIVEN, is_given
from spryx_http import SpryxAsyncClient

from spryx_agents.types.vector_store import VectorFileStatus


class VectorStores:
    def __init__(self, client: SpryxAsyncClient):
        self._client = client

    async def list_vector_stores(
        self,
        page: int = 1,
        limit: int = 10,
        order: str = "asc",
    ) -> dict:
        """List all vector stores."""
        return await self._client.get(
            "/v1/vector-stores",
            params={"page": page, "limit": limit, "order": order},
        )

    async def create_vector_store(
        self,
        name: str,
        description: str,
    ) -> dict:
        """Create a new vector store."""
        payload = {
            "name": name,
            "description": description,
        }

        return await self._client.post("/v1/vector-stores", json=payload)

    async def get_vector_store(
        self,
        vector_store_id: str,
    ) -> dict:
        """Retrieve a specific vector store by ID."""
        return await self._client.get(f"/v1/vector-stores/{vector_store_id}")

    async def add_file_to_vector_store(
        self,
        vector_store_id: str,
        file_id: str,
    ) -> dict:
        """Add a file to a vector store."""
        payload = {
            "file_id": file_id,
        }

        return await self._client.post(
            f"/v1/vector-stores/{vector_store_id}/files",
            json=payload,
        )

    async def update_vector_file(
        self,
        vector_store_id: str,
        file_id: str,
        status: VectorFileStatus,
        organization_id: str,
        failed_reason: str = NOT_GIVEN,
        tokens_size: int = NOT_GIVEN,
    ) -> dict:
        """Update a vector file status."""
        payload = {"status": status.value}

        if is_given(failed_reason):
            payload["failed_reason"] = failed_reason

        if is_given(tokens_size):
            payload["tokens_size"] = tokens_size

        return await self._client.put(
            f"/v1/vector-stores/{vector_store_id}/files/{file_id}",
            json=payload,
            headers={"x-organization-id": organization_id},
        )
