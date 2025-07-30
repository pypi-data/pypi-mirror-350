from spryx_http import SpryxAsyncClient


class EmbeddingUsages:
    def __init__(self, client: SpryxAsyncClient):
        self.client = client

    async def add_embedding_usage(
        self,
        organization_id: str,
        vector_store_id: str,
        model: str,
        embedding_tokens: int,
        embedding_requests: int,
    ) -> list[dict]:
        return await self.client.post(
            "/v1/embedding-usages",
            json={
                "kind": "add_text",
                "vector_store_id": vector_store_id,
                "model": model,
                "embedding_tokens": embedding_tokens,
                "embedding_requests": embedding_requests,
            },
            headers={"x-organization-id": organization_id},
        )
