
from wetro.api_client import WetrocloudClient
from wetro.rag import WetroRAG
from wetro.toolkit import WetroTools
from typing import List,Optional,Union, Any
from wetro.custom_types import ChatModel, ResourceType, Categories, JSONSchema, Message, URL, MarkdownResourceType, TranscribeResourceType
from wetro.custom_response import CategorizeResponse, GenerateTextResponse, ImageToTextResponse, ExtractDataResponse, MarkdownCoverterResponse, TrascribeResponse

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
        self.collection = self.rag.collection

    def categorize(
            self, 
            resource: str, 
            type: ResourceType, 
            json_schema: JSONSchema, 
            categories: Categories,
            prompt: str
        ) -> CategorizeResponse:
        """
        Categories your resource.
        """
        return self.tools.categorize(resource, type, json_schema, categories, prompt)

    def generate_text(
            self, 
            messages: List[Message], 
            model: ChatModel
        ) -> GenerateTextResponse:
        """
        Generate Text-Response based on message
        """
        return self.tools.generate_text(messages, model)

    def image_to_text(
            self, 
            image_url: URL, 
            request_query: str
        ) -> ImageToTextResponse:
        """
        Generate Text-Response based on image
        """
        return self.tools.image_to_text(image_url, request_query)

    def extract(
            self, 
            website: URL, 
            json_schema: JSONSchema
        ) -> ExtractDataResponse:
        """
        Extract Data from Websites
        """
        return self.tools.extract(website, json_schema)
    
    def markdown_converter(
            self, 
            link: Union[str, bytes, Any], 
            resource_type : MarkdownResourceType
        ) -> MarkdownCoverterResponse:
        """
        Convert Data to Markdown
        """
        return self.tools.markdown_converter(link, resource_type )
    
    def transcript(
            self, 
            link: URL, 
            resource_type : TranscribeResourceType
        ) -> TrascribeResponse:
        """
        Trascribe Youtube Videos
        """
        return self.tools.transcript(link, resource_type )
    