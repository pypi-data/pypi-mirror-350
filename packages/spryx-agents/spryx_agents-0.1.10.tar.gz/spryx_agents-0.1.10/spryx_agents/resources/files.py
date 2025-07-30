from spryx_core import NOT_GIVEN, is_given
from spryx_http import SpryxAsyncClient


class Files:
    def __init__(self, client: SpryxAsyncClient):
        self._client = client

    async def presign_upload(
        self,
        file_name: str,
        content_type: str,
    ) -> dict:
        """Get a pre-signed URL for file upload."""
        payload = {
            "file_name": file_name,
            "content_type": content_type,
        }

        return await self._client.post(
            "/files/presign/upload",
            json=payload,
        )

    async def add_file(
        self,
        object_key: str,
    ) -> dict:
        """Add a file using the object key from a successful upload."""
        payload = {
            "object_key": object_key,
        }

        return await self._client.post("/files", json=payload)

    async def get_file(
        self,
        file_id: str,
    ) -> dict:
        """Retrieve a file by ID."""
        return await self._client.get(f"/files/{file_id}") 