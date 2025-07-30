import logging
from wetro.api_client import WetrocloudClient
from typing import List,Optional
from wetro.custom_types import ChatModel, ResourceType, Categories, JSONSchema, Message, URL
from wetro.custom_response import CategorizeResponse, GenerateTextResponse, ImageToTextResponse, ExtractDataResponse

class WetroTools:
    """
    Client for additional tools provided by Wetrocloud Outside RAG.
    
    Usage:
        tools_client = WetroTools(api_key="your_api_key")
        res = tools_client.categorize(
            resource="match review: John Cena vs. The Rock.",
            type="text",
            json_schema='{"label": "string"}',
            categories=["wrestling", "entertainment"]
        )
        res = tools_client.generate_text(
            messages=[{"role": "user", "content": "What is a large language model?"}],
            model="gpt-4"
        )
        res = tools_client.image_to_text(
            image_url="https://example.com/image.jpg",
            request_query="What animal is this?"
        )
        res = tools_client.extract(
            website="https://www.forbes.com/real-time-billionaires/",
            json_schema='[{"name": "<name>", "networth": "<networth>"}]'
        )
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

    def categorize(
            self, 
            resource: str, 
            type: ResourceType, 
            json_schema: JSONSchema, 
            categories: Categories
        ) -> CategorizeResponse:
        """
        Categories your resource.
        """
        return self._client.categorize_data(resource, type, json_schema, categories)

    def generate_text(
            self, 
            messages: List[Message], 
            model: ChatModel
        ) -> GenerateTextResponse:
        """
        Generate Text-Response based on message
        """
        return self._client.generate_text(messages, model)

    def image_to_text(
            self, 
            image_url: URL, 
            request_query: str
        ) -> ImageToTextResponse:
        """
        Generate Text-Response based on image
        """
        return self._client.image_to_text(image_url, request_query)

    def extract(
            self, 
            website: URL, 
            json_schema: JSONSchema
        ) -> ExtractDataResponse:
        """
        Extract Data from Websites
        """
        return self._client.extract_data(website, json_schema)
    
