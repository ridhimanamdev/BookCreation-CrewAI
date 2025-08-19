from typing import List
from pydantic import BaseModel

# Define the data models for the book outline
# These models can be used to structure the data for the book outline

class ChapterOutline(BaseModel):
    title: str
    content: str


class BookOutline(BaseModel):
    chapters: List[ChapterOutline]

