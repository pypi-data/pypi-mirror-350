import json
import requests
import logging
from typing import Any, Dict, List, Optional, Iterable, Union
from wetro.custom_types import (
    ChatModel, 
    ResourceType, 
    ChatHistory, 
    JSONSchema, 
    Categories, 
    CollectionID, 
    ResourceID, 
    URL, 
    Message
    )
from wetro.custom_response import (
    CreateCollectionResponse, 
    GetCollectionResponse,
    QueryResponse, 
    ChatResponse, 
    InsertResponse, 
    RemoveResponse, 
    DeleteCollectionResponse, 
    CategorizeResponse, 
    GenerateTextResponse, 
    ImageToTextResponse, 
    ExtractDataResponse,
    WetrocloudAPIResponse
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wetrocloud")

class WetrocloudAPIError(Exception):
    """Custom exception for Wetrocloud API errors."""
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload

class WetrocloudClient:
    """
    A client for interacting with the Wetrocloud API.
    
    Attributes:
        api_key (str): Your API key for authenticating with the Wetrocloud API.
        base_url (str): The base URL for the Wetrocloud API endpoints.
        timeout (int): The timeout for HTTP requests (in seconds).
    """
    def __init__(
            self, 
            api_key: str, 
            base_url: str = "https://api.wetrocloud.com", 
            timeout: int = 30
        ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")  # Ensure no trailing slash
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json",
        }
        logger.info("WetrocloudClient initialized with base_url: %s", self.base_url)

    def _parse_error(self, response: requests.Response) -> str:
        """Helper to extract error messages from the response."""
        try:
            error_data = response.json()
        except ValueError:
            return response.text or "Unknown error"
        
        # Check for common error keys
        if "error" in error_data:
            return error_data["error"]
        if "detail" in error_data:
            return error_data["detail"]
        # For missing parameter errors, join messages together.
        if isinstance(error_data, dict):
            errors = []
            for field, messages in error_data.items():
                if isinstance(messages, list):
                    errors.append(f"{field}: {', '.join(messages)}")
                else:
                    errors.append(f"{field}: {messages}")
            return "; ".join(errors)
        return str(error_data)

    def _request(
            self, 
            method: str, 
            endpoint: str, 
            params: dict = None, 
            data: dict = None, 
            response_model: Optional[Any] = None
        ) -> Any:
        """
        Internal method to make HTTP requests to the API.
        Sends JSON data.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE).
            endpoint (str): API endpoint (e.g., '/v1/create/').
            params (dict, optional): Query parameters.
            data (dict, optional): Request body.
        
        Returns:
            dict: Parsed JSON response.
        
        Raises:
            WetrocloudAPIError: If the request fails.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            logger.debug("Making %s request to %s with params=%s and data=%s", method, url, params, data)
            response = requests.request(method, url, headers=self.headers, params=params, json=data, timeout=self.timeout)
            response.raise_for_status()
            json_response = response.json()
            logger.debug("Response received: %s", json_response)
            if response_model is not None:
                return response_model.model_validate(json_response)
            return WetrocloudAPIResponse(json_response)
        except requests.exceptions.HTTPError as http_err:
            error_msg = self._parse_error(http_err.response)
            logger.error("HTTP error occurred: %s", error_msg)
            raise WetrocloudAPIError(f"HTTP error occurred: {error_msg}", status_code=http_err.response.status_code, payload=http_err.response.json())
        except requests.exceptions.RequestException as req_err:
            logger.error("Request exception: %s", req_err)
            raise WetrocloudAPIError(f"Request exception: {req_err}")

    def _request_multipart(
            self, 
            method: str, 
            endpoint: str, 
            data: dict, 
            response_model: Optional[Any] = None
        ) -> WetrocloudAPIResponse:
        """
        Internal method to make multipart/form-data requests.
        Used for endpoints that require form data instead of JSON (e.g. chat and remove-resource).
        
        Args:
            method (str): HTTP method (POST or DELETE).
            endpoint (str): API endpoint.
            data (dict): Form data parameters.
        
        Returns:
            dict: Parsed JSON response.
        
        Raises:
            WetrocloudAPIError: If the request fails.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            # Only the Authorization header is needed; let requests set the Content-Type automatically.
            headers = {"Authorization": self.headers["Authorization"]}
            # Prepare multipart form data; if a value is not a string, convert it to JSON.
            files = {k: (None, v if isinstance(v, str) else json.dumps(v)) for k, v in data.items()}
            logger.debug("Making multipart %s request to %s with data=%s", method, url, data)
            response = requests.request(method, url, headers=headers, files=files, timeout=self.timeout)
            response.raise_for_status()
            json_response = response.json()
            logger.debug("Multipart response received: %s", json_response)
            if response_model is not None:
                return response_model.model_validate(json_response)
            return WetrocloudAPIResponse(json_response)
        except requests.exceptions.HTTPError as http_err:
            error_msg = self._parse_error(http_err.response)
            logger.error("HTTP error in multipart request: %s", error_msg)
            raise WetrocloudAPIError(f"HTTP error occurred: {error_msg}", status_code=http_err.response.status_code, payload=http_err.response.json())
        except requests.exceptions.RequestException as req_err:
            logger.error("Request exception in multipart request: %s", req_err)
            raise WetrocloudAPIError(f"Request exception: {req_err}")

    def _request_stream(
            self,
            method: str,
            endpoint: str,
            params: dict = None,
            data: dict = None,
            response_model: Optional[Any] = None
        ) -> Iterable[Any]:
        url = f"{self.base_url}{endpoint}"
        try:
            logger.debug("Making streaming %s request to %s with params=%s and data=%s", method, url, params, data)
            response = requests.request(method, url, headers=self.headers, params=params, json=data, timeout=self.timeout, stream=True)
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if response_model is not None:
                        yield response_model.model_validate(chunk)
                    else:
                        yield chunk
        except requests.exceptions.HTTPError as http_err:
            error_msg = self._parse_error(http_err.response)
            logger.error("HTTP error in streaming request: %s", error_msg)
            raise WetrocloudAPIError(
                f"HTTP error occurred: {error_msg}",
                status_code=http_err.response.status_code,
                payload=http_err.response.json()
            )
        except requests.exceptions.RequestException as req_err:
            logger.error("Request exception in streaming request: %s", req_err)
            raise WetrocloudAPIError(f"Request exception: {req_err}")

    # --- New functions for collection endpoints ---
    def create_collection(
            self,
            collection_id: CollectionID
        ) -> CreateCollectionResponse:
        """
            Create a new collection.

            Endpoint:
                POST /v1/collection/create/ (&#8203;:contentReference[oaicite:6]{index=6})
        """
        payload = {
            "collection_id": collection_id,
        }
        logger.info("Creating a new collection")
        return self._request("POST", "/v1/collection/create/",data=payload, response_model=CreateCollectionResponse)
    
    def get_collection(self, collection_id: CollectionID) -> GetCollectionResponse:
        """
            Get a new collection.

            Endpoint:
                POST /v1/collection/get/<collection_id>/ (&#8203;:contentReference[oaicite:6]{index=6})
        """
        endpoint = f"/v1/collection/get/{collection_id}/"
        logger.info("Checking existence of collection %s", collection_id)
        return self._request("GET", endpoint, response_model=GetCollectionResponse)

    def query_collection(
            self, 
            collection_id: CollectionID, 
            request_query: str, 
            model: Optional[ChatModel] = None,
            json_schema: Optional[JSONSchema] = None,
            json_schema_rules: Optional[List[str]] = None,
            stream: bool = False
        ) -> Union[QueryResponse, Iterable[QueryResponse]]:
        """
        Query a collection for answers.
        
        Args:
            collection_id (str): The collection ID.
            request_query (str): The query string.
            model (str, optional): Optional model identifier.
        
        Returns:
            dict: Response including the query answer, tokens, and success flag.
        
        Endpoint:
            POST /v1/query/ (&#8203;:contentReference[oaicite:8]{index=8})
        """
        payload = {
            "collection_id": collection_id,
            "request_query": request_query
        }
        if model:
            payload["model"] = model
        # Enforce that both json_schema and json_schema_rules are provided together.
        # Validate structured output parameters
        if (json_schema is not None or json_schema_rules is not None) and stream:
            raise ValueError("Streaming mode does not support json_schema and json_schema_rules.")
        if (json_schema is not None and json_schema_rules is None) or (json_schema_rules is not None and json_schema is None):
            raise ValueError("Both json_schema and json_schema_rules must be provided together, or neither.")
        if json_schema is not None and json_schema_rules is not None:
            payload["json_schema"] = json_schema
            payload["json_schema_rules"] = json_schema_rules
        if stream:
            payload["stream"] = True
            return self._request_stream("POST", "/v1/collection/query/", data=payload, response_model=QueryResponse)
        else:
            return self._request("POST", "/v1/collection/query/", data=payload, response_model=QueryResponse)

    def chat_with_collection(
            self, 
            collection_id: CollectionID, 
            message: str, 
            chat_history: ChatHistory = [], 
            model: Optional[ChatModel] = None,
            stream: bool = False  
        ) -> Union[QueryResponse, Iterable[ChatResponse]]:
        """
        Chat with a collection to have a conversation based on its resources.
        
        Args:
            collection_id (str): The collection ID.
            message (str): The current message.
            chat_history (List[dict]): A list of previous chat messages (each a dict with 'role' and 'content').
        
        Returns:
            dict: Response including the conversational reply, tokens, and success flag.
        
        Endpoint:
            POST /v1/collection/chat/ (&#8203;:contentReference[oaicite:9]{index=9})
        """
        form_data = {
            "collection_id": collection_id,
            "message": message,
            "chat_history": chat_history
        }
        if model:
            form_data["model"] = model
        logger.info("Chatting with collection %s, message: %s", collection_id, message)
        if stream:
            form_data["stream"] = True
            return self._request_stream("POST", "/v1/collection/chat/", data=form_data, response_model=ChatResponse)
        else:
            return self._request("POST", "/v1/collection/chat/", data=form_data, response_model=ChatResponse)

    def insert_resource(
            self, 
            collection_id: CollectionID, 
            resource: str, 
            type: ResourceType
        ) -> InsertResponse:
        """
            Insert a resource into a collection.
            
            Args:
                collection_id (str): The ID of the collection.
                resource (str): The resource URL, text, file URL, etc.
                type (str): The type of resource (e.g., 'web', 'file', 'text', 'json', 'youtube').
            
            Returns:
                dict: Response including success flag and tokens used.
            
            Endpoint:
                POST /v1/insert/ (&#8203;:contentReference[oaicite:7]{index=7})
        """
        payload = {
            "collection_id": collection_id,
            "resource": resource,
            "type": type
        }
        logger.info("Inserting resource into collection %s", collection_id)
        return self._request("POST", "/v1/resource/insert/", data=payload, response_model=InsertResponse)
    
    def remove_resource(
            self,
            collection_id: CollectionID, 
            resource_id: ResourceID
        ) -> RemoveResponse:
        """
        Remove a resource from a collection.
        
        Args:
            collection_id (str): The collection ID.
            resource_id (str): The resource ID to remove.
        
        Returns:
            dict: Response indicating whether the removal was successful.
        
        Endpoint:
            DELETE /v1/remove/resource/ (&#8203;:contentReference[oaicite:10]{index=10})
        """
        form_data = {
            "collection_id": collection_id,
            "resource_id": resource_id
        }
        logger.info("Removing resource %s from collection %s", resource_id, collection_id)
        return self._request_multipart("DELETE", "/v1/resource/remove/", data=form_data, response_model=RemoveResponse)

    def delete_collection(
            self, 
            collection_id: CollectionID
        ) -> DeleteCollectionResponse:
        """
        Delete a collection.
        
        Args:
            collection_id (str): The ID of the collection to delete.
        
        Returns:
            dict: Response including a message and success flag.
        
        Endpoint:
            DELETE /v1/delete/ (&#8203;:contentReference[oaicite:11]{index=11})
        """
        payload = {
            "collection_id": collection_id
        }
        logger.info("Deleting collection %s", collection_id)
        return self._request("DELETE", "/v1/collection/delete/", data=payload, response_model=DeleteCollectionResponse)
    
     # New functions for additional endpoints

    def categorize_data(
            self, 
            resource: str, 
            type: ResourceType, 
            json_schema: JSONSchema, 
            categories: Categories
        ) -> CategorizeResponse:
        """
        Categorize a resource using a JSON schema and rules.
        
        Endpoint: POST /v1/categorize/
        """
        payload = {
            "resource": resource,
            "type": type,
            "json_schema": json_schema,
            "categories": categories
        }
        return self._request("POST", "/v1/categorize/", data=payload, response_model=CategorizeResponse)

    def generate_text(
            self, 
            messages: List[Message], 
            model: ChatModel
        ) -> GenerateTextResponse:
        """
        Generate text using the provided conversation messages and model.
        
        Endpoint: POST /v1/text-generation/
        Note: This endpoint expects multipart/form-data.
        """
        form_data = {
            "messages": messages,  # Can be a list of message objects
            "model": model
        }
        return self._request("POST", "/v1/text-generation/", data=form_data, response_model=GenerateTextResponse)

    def image_to_text(
            self, 
            image_url: URL, 
            request_query: str
        ) -> ImageToTextResponse:
        """
        Convert an image to text (OCR) and optionally answer a query about the image.
        
        Endpoint: POST /v1/image-to-text/
        """
        payload = {
            "image_url": image_url,
            "request_query": request_query
            }
        return self._request("POST", "/v1/image-to-text/", data=payload, response_model=ImageToTextResponse)

    def extract_data(
            self, 
            website: URL, 
            json_schema: JSONSchema
        ) -> ExtractDataResponse:
        """
        Extract structured data from a website using the provided JSON schema.
        
        Endpoint: POST /v1/data-extraction/
        Note: This endpoint expects multipart/form-data.
        """
        form_data = {
            "website": website,
            "json_schema": json_schema
        }
        return self._request("POST", "/v1/data-extraction/", data=form_data, response_model=ExtractDataResponse)


# Example usage:
if __name__ == "__main__":
    # Replace 'your_api_key_here' with your actual API key
    client = WetrocloudClient(api_key="c80d5cb1f295297ef77eb82f42aafe09b71625e1",base_url="http://127.0.0.1:8000/")
    
    try:
        # Create a new collection
        # create_response = client.create_collection("sdk_unique_id_3")
        # logger.info("Collection Created: %s", create_response)
        # collection_id = create_response.collection_iD
        # print(create_response.collection_id)
        
        # if collection_id:
        #     # collection_id = "sdk_unique_id_1"
        # #     # Insert a resource into the collection
        #     insert_response = client.insert_resource(
        #         collection_id=collection_id,
        #         resource="https://medium.com/@wetrocloud/rag-vs-fine-tuning-which-one-should-you-use-for-your-ai-workflow-5a71fc56ed77",
        #         type="web"
        #     )
        #     resource_id = insert_response.resource_id
        #     logger.info("Resource Inserted: %s", insert_response)
            
        # #     # Query the collection for an answer
        #     query_response = client.query_collection(
        #         collection_id=collection_id,
        #         request_query="What are the key points of the article?"
        #     )
        #     logger.info("Query Response: %s", query_response)
            
        #     # Chat with the collection
            
        #     chat_history = [
        #         {"role": "user", "content": "What is this collection about?"},
        #         {"role": "system", "content": "It stores web articles and documents."}
        #     ]
        #     chat_response = client.chat_with_collection(
        #         collection_id=collection_id,
        #         message="Can you summarize the content?",
        #         chat_history=chat_history
        #     )
        #     logger.info("Chat Response: %s", chat_response)
            
        #     # Remove a resource (example resource_id; replace with a real one)
        #     remove_response = client.remove_resource(
        #         collection_id=collection_id,
        #         resource_id=resource_id
        #     )
        #     logger.info("Resource Removal: %s", remove_response)
            
        #     # Delete the collection when done
        #     delete_response = client.delete_collection(collection_id)
        #     logger.info("Collection Deletion: %s", delete_response)

        # # Data categorization example:
        category_response = client.categorize_data(
            resource="match review: John Cena vs. The Rock.",
            type="text",
            json_schema="{\"label\":\"string\"}",
            categories=["football", "coding", "entertainment", "basketball", "wrestling", "information"]
        )
        print(category_response.response)
        
        # Text generation example:
        messages = [{"role": "user", "content": "what is a large language model?"}]
        text_gen_response = client.generate_text(messages, model="llama-3.3-70b")
        print(text_gen_response.response)
        
        # Image to text (OCR) example:
        image_response = client.image_to_text(
            image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQBQcwHfud1w3RN25Wgys6Btt_Y-4mPrD2kg&s",
            request_query="What animal is this?"
        )
        print(image_response.response)
        
        # Data extraction example:
        extraction_response = client.extract_data(
            website="https://www.forbes.com/real-time-billionaires/#7583ee253d78",
            json_schema='[{"name":"<name of rich man>", "networth":"<amount worth>"}]'
        )
        print(extraction_response.response)

        
    except WetrocloudAPIError as e:
        logger.error("An error occurred: %s", e)
