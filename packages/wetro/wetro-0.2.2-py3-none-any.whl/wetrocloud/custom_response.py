from typing import Union, Dict, Any,Optional
from pydantic import BaseModel
from wetro.custom_types import CollectionID,ResourceID, JSONSchema

class CreateCollectionResponse(BaseModel):
    collection_id: CollectionID
    success: bool

class GetCollectionResponse(BaseModel):
    success: bool
    found: bool
    collection_id: Optional[str] = None

class QueryResponse(BaseModel):
    response: Union[str, JSONSchema]
    tokens: int
    success: bool

class ChatResponse(BaseModel):
    response: Union[str, JSONSchema]
    tokens: int
    success: bool

class InsertResponse(BaseModel):
    resource_id : ResourceID
    success: bool
    tokens: Optional[int] = None

class RemoveResponse(BaseModel):
    success: bool

class DeleteCollectionResponse(BaseModel):
    message: str
    success: bool

class CategorizeResponse(BaseModel):
    response: JSONSchema
    tokens: int
    success: bool

class GenerateTextResponse(BaseModel):
    response: Union[str, JSONSchema]
    tokens: int
    success: bool

class ImageToTextResponse(BaseModel):
    response: str
    tokens: int
    success: bool

class ExtractDataResponse(BaseModel):
    response: JSONSchema
    tokens: int
    success: bool


class WetrocloudAPIResponse:
    def __init__(self, data: Dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
