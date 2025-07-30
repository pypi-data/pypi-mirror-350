import logging
from wetro.api_client import WetrocloudClient
from wetro.rag import WetroRAG
from wetro.toolkit import WetroTools


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wetrocloud")

class Wetrocloud:
    """
    Client that allows setting the API key only once.
    
    Usage:
        client = Wetrocloud(api_key="your_api_key")
        rag_client = client.rag
        tools_client = client.tools
    """
    def __init__(
            self, 
            api_key: str, 
            base_url: str = "https://api.wetrocloud.com", 
            timeout: int = 30
        ):
        self._client = WetrocloudClient(api_key, base_url, timeout)
        self.rag = WetroRAG(client=self._client)
        self.tools = WetroTools(client=self._client)

if __name__ == "__main__":
    pass
    rag_client = WetroRAG(api_key="c80d5cb1f295297ef77eb82f42aafe09b71625e1",base_url="http://127.0.0.1:8000/")
    rag_client.collection.get_or_create_collection_id("sdk_unique_id_5")
    query_response = rag_client.collection.query("What are the key points of the article?")
    print(query_response)