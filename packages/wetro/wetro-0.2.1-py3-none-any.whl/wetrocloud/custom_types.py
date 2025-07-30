from typing import Any, Dict, List, Union
from typing_extensions import Literal, TypedDict, TypeAlias
# Custom type definitions
ChatModel: TypeAlias = Literal[
    "chatgpt-4o-latest", 
    "claude-3-5-haiku-20241022", 
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-20241022", 
    "claude-3-7-sonnet-20250219", 
    "claude-3-haiku-20240307",
    "claude-3-opus-20240229", 
    "claude-3-sonnet-20240229", 
    "deepseek-r1-distill-llama-70b",
    "deepseek-r1-distill-llama-70b-specdec", 
    "deepseek-r1-distill-qwen-32b", 
    "gpt-3.5-turbo",
    "gpt-4", 
    "gpt-4-turbo", 
    "gpt-4-turbo-preview", 
    "gpt-4.5-preview", 
    "gpt-4o", 
    "gpt-4o-mini",
    "llama-3.1-8b", 
    "llama-3.1-8b-instant", 
    "llama-3.2-1b-preview", 
    "llama-3.2-3b-preview",
    "llama-3.2-11b-vision-preview", 
    "llama-3.2-90b-vision-preview", 
    "llama-3.3-70b",
    "llama-3.3-70b-specdec", 
    "llama-3.3-70b-versatile", 
    "llama3-70b-8192", 
    "llama3-8b-8192",
    "llama-guard-3-8b", 
    "mixtral-8x7b-32768", 
    "o1", 
    "o1-mini", 
    "o1-preview", 
    "o3-mini",
    "qwen-2.5-32b", 
    "qwen-2.5-coder-32b"
]

ResourceType: TypeAlias = Literal["text", "web", "file", "json", "youtube"]


class Message(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str

ChatHistory: TypeAlias = List[Message]

JSONSchema: TypeAlias = Union[None, bool, int, float, str, List[Any], Dict[str, Any]]
Categories: TypeAlias = List[str]

CollectionID: TypeAlias = str
ResourceID: TypeAlias = str
URL: TypeAlias = str
