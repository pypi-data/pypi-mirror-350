from spryx_http import SpryxAsyncClient


class Integrations:
    def __init__(self, client: SpryxAsyncClient):
        self._client = client

    async def list_integrations(self) -> dict:
        """List all available integrations."""
        return await self._client.get("/v1/integrations/") 