import logging
from wetro.collection import CollectionAPI
from wetro.api_client import WetrocloudClient
from typing import Optional



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("user")

class WetroRAG:
    """
    Client for collection-based Retrieval-Augmented Generation (RAG).
    
    Usage:
        rag_client = WetroRAG(api_key="your_api_key")
        rag_client.collection.get_or_create_collection_id("collection_id")
        rag_client.collection.insert(resource="https://example.com", type="web")
        response = rag_client.collection.query(request_query="query message")
        response = rag_client.collection.chat(message="message", chat_history=[])
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.wetrocloud.com",
        timeout: int = 30,
        client: Optional[WetrocloudClient] = None
    ):
        if client is None:
            if api_key is None:
                raise ValueError("Must provide either an API key or a client instance")
            self._client = WetrocloudClient(api_key, base_url, timeout)
        else:
            self._client = client
        self.collection = CollectionAPI(self._client)
