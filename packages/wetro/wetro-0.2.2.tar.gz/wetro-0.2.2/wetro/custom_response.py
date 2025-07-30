from typing import Union, Dict, Any,Optional,List
from pydantic import BaseModel
from wetro.custom_types import CollectionID,ResourceID, JSONSchema, CollectionItem, InsertStatus

class CreateCollectionResponse(BaseModel):
    collection_id: CollectionID
    success: bool

class GetCollectionResponse(BaseModel):
    success: bool
    found: bool
    collection_id: Optional[str] = None

class ListCollectionResponse(BaseModel):
    count: Optional[int] = None
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[CollectionItem]

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
    status: Optional[InsertStatus] = None

class CheckInsertResponse(BaseModel):
    resource_id : ResourceID
    success: bool
    status: Optional[InsertStatus] = None

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

class MarkdownCoverterResponse(BaseModel):
    response: str
    tokens: int
    success: bool


class TrascribeResponse(BaseModel):
    response: JSONSchema
    tokens: int
    success: bool

class WetrocloudAPIResponse:
    def __init__(self, data: Dict[str, Any]):
        for key, value in data.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
