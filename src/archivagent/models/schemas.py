from pydantic import BaseModel, Field
from typing import List, Literal
class AcademicAuthor(BaseModel):
    name: str

class LiteratureCategorization(BaseModel):
    title: str = Field(..., description="The exact title of the publication.")
    authors: List[AcademicAuthor]
    venue: str = Field(..., description="The confrence or journal of publication.")
    year: int

    category: Literal["Books & Guides", "Papers & Articles"] = Field(..., description="Strict classification of the literature.")
    abstraction: str | None = Field(None, description="Detailed abstraction of summary of the academic work.")
