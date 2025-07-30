from spryx_core import NOT_GIVEN, is_given
from spryx_http import SpryxAsyncClient


class Chats:
    def __init__(self, client: SpryxAsyncClient):
        self._client = client

    async def list_chats(
        self,
        page: int = 1,
        limit: int = 10,
        order: str = "asc",
    ) -> dict:
        """List all chats."""
        return await self._client.get(
            "/chats/",
            params={"page": page, "limit": limit, "order": order},
        )

    async def get_chat(
        self,
        chat_id: str,
    ) -> dict:
        """Retrieve a chat by ID."""
        return await self._client.get(f"/chats/{chat_id}")

    async def update_chat(
        self,
        chat_id: str,
        name: str,
        description: str,
        private: bool,
    ) -> dict:
        """Update a chat."""
        payload = {
            "name": name,
            "description": description,
            "private": private,
        }

        return await self._client.put(
            f"/chats/{chat_id}",
            json=payload,
        )

    async def list_messages(
        self,
        chat_id: str,
        page: int = 1,
        limit: int = 10,
        order: str = "asc",
    ) -> dict:
        """List all messages in a chat."""
        return await self._client.get(
            f"/chats/{chat_id}/messages",
            params={"page": page, "limit": limit, "order": order},
        ) 