from pydantic import BaseModel
from typing import List, Optional


class Category(BaseModel):
    id: int
    name: str


class Tag(BaseModel):
    id: int
    name: str


class Pet(BaseModel):
    name: str
    photoUrls: List[str]
    id: Optional[int] = None
    category: Optional[Category] = None
    tags: Optional[List[Tag]] = None
    status: Optional[str] = None
