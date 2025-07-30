from spryx_http import SpryxAsyncClient

from spryx_agents.resources.agents import Agents
from spryx_agents.resources.chats import Chats
from spryx_agents.resources.credential_types import CredentialTypes
from spryx_agents.resources.credentials import Credentials
from spryx_agents.resources.embedding_usages import EmbeddingUsages
from spryx_agents.resources.files import Files
from spryx_agents.resources.integrations import Integrations
from spryx_agents.resources.vector_stores import VectorStores


class SpryxAgents(SpryxAsyncClient):
    def __init__(
        self,
        application_id: str,
        application_secret: str,
        base_url: str = "https://dev-agents.spryx.ai",
        iam_base_url: str = "https://dev-iam.spryx.ai",
    ):
        super().__init__(
            base_url=base_url,
            iam_base_url=iam_base_url,
            application_id=application_id,
            application_secret=application_secret,
        )

        self.agents = Agents(self)
        self.chats = Chats(self)
        self.credential_types = CredentialTypes(self)
        self.credentials = Credentials(self)
        self.files = Files(self)
        self.integrations = Integrations(self)
        self.vector_stores = VectorStores(self)
        self.embedding_usages = EmbeddingUsages(self)
