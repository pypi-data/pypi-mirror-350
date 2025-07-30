from pydantic import BaseModel
from typing import Optional


class ESPropertySearch(BaseModel):
    query_vector: Optional[list[float]] = None
    prompt: str
    k: int = 10
    num_candidates: int = 10
    index: str = "property_embeddings"
    source: list[str] = ["title", "description", "text", "keywords", "property_id", "user_id", "date"]


