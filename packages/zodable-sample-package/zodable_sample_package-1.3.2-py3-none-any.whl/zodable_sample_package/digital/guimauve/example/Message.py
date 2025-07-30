from pydantic import BaseModel
from typing import Generic
from typing import TypeVar

T = TypeVar('T')
class Message(BaseModel, Generic[T]):
    content: T
