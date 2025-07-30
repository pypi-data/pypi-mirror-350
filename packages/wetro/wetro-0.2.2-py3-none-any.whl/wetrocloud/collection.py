import logging
from wetro.api_client import WetrocloudClient
from typing import Optional,List, Union, Iterable
from wetro.custom_types import (
    ChatModel, 
    ResourceType, 
    ChatHistory, 
    JSONSchema, 
    CollectionID, 
    ResourceID
    )
from wetro.custom_response import (
    QueryResponse, 
    ChatResponse, 
    InsertResponse, 
    RemoveResponse, 
    DeleteCollectionResponse
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wetrocloud")

class CollectionAPI:
    """
    Interface for collection operations.
    """
    def __init__(
            self, 
            client: WetrocloudClient
        ):
        self.client = client
        self.collection_id: Optional[CollectionID] = None

    def get_or_create_collection_id(
            self, 
            collection_id: CollectionID
        ) -> None:
        """
        Check if the collection exists and get collection; if not, create a new collection.
        """
        get_response = self.client.get_collection(collection_id)
        if get_response.found:
            self.collection_id = get_response.collection_id
            logger.info("Found existing collection: %s", self.collection_id)
        else:
            create_response = self.client.create_collection(collection_id)
            self.collection_id = create_response.collection_id
            logger.info("Created new collection: %s", self.collection_id)

    def insert(
            self, 
            resource: str, 
            type: ResourceType
        ) -> InsertResponse:
        """
        Inserts resource into a collection.
        """
        if not self.collection_id:
            raise ValueError("Collection ID not set. Please call get_or_create_collection_id() first.")
        return self.client.insert_resource(self.collection_id, resource, type)
    
    def delete_resource(
            self, 
            resource_id: ResourceID
        ) -> RemoveResponse:
        """
        Removes resource from a collection.
        """
        if not self.collection_id:
            raise ValueError("Collection ID not set. Please call set_or_create_collection_id() first.")
        return self.client.remove_resource(self.collection_id, resource_id)

    def query(
            self, 
            request_query: str, 
            model: Optional[ChatModel] = None,
            json_schema: Optional[JSONSchema] = None,
            json_schema_rules: Optional[List[str]] = None,
            stream: bool = False
            ) -> Union[QueryResponse, Iterable[QueryResponse]]:
        """
        Query your collection.
        """
        if not self.collection_id:
            raise ValueError("Collection ID not set. Please call set_or_create_collection_id() first.")
        return self.client.query_collection(
            self.collection_id,
            request_query,
            model=model,
            json_schema=json_schema,
            json_schema_rules=json_schema_rules,
            stream=stream
        )

    def chat(
            self, 
            message: str, 
            chat_history: ChatHistory, 
            model: Optional[ChatModel] = None,
            stream: bool = False
        ) -> Union[QueryResponse, Iterable[ChatResponse]]:
        """
        Chat with your collection.
        """
        if not self.collection_id:
            raise ValueError("Collection ID not set. Please call set_or_create_collection_id() first.")
        return self.client.chat_with_collection(
            self.collection_id, 
            message, 
            chat_history, 
            model=model,
            stream=stream
            )

    def delete(self) -> DeleteCollectionResponse:
        """
        Delete your collection.
        """
        if not self.collection_id:
            raise ValueError("Collection ID not set. Cannot delete a non-existent collection.")
        response = self.client.delete_collection(self.collection_id)
        self.collection_id = None
        return response
