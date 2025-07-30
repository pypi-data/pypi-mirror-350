from pydantic import BaseModel, Field, field_validator, ValidationInfo
from datetime import datetime
from typing import List, Optional, Any, Callable
import uuid
import json
import ast


class CreateElasticPropertyEmbeddingDTO(BaseModel):
    vector: List[float]
    text: str
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    doc_id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4) 
    id: Optional[int] = None
    date: Optional[datetime] = Field(default_factory=datetime.now)
    index_name: str = "property_embeddings"
    user_id: Optional[int] = None
    property_id: Optional[int] = None

    @classmethod
    def _parse_string_to_list(cls, v: Any, item_caster: Callable, field_name: str) -> Any:
        """
        Helper to parse a string (JSON array or comma-separated) into a list.
        Returns the original value if not a string, allowing Pydantic to handle other cases.
        """
        if not isinstance(v, str):
            return v # Not a string, Pydantic will validate (e.g., if already a list or wrong type)

        if not v.strip(): # Empty or whitespace-only string becomes an empty list
            return []

        # Attempt 1: JSON array
        try:
            data = json.loads(v)
            if isinstance(data, list):
                return [item_caster(item) for item in data]
            else:
                # Parsed as JSON, but not a list. This is an invalid format for our purpose.
                raise ValueError("Parsed JSON is not a list.")
        except json.JSONDecodeError:
            # Not a valid JSON string, proceed to Attempt 2: Comma-separated
            pass 
        except Exception as e: # Catch errors from item_caster during JSON list processing
            raise ValueError(f"Field '{field_name}': Error casting items from JSON list '{v}'. Error: {e}")

        # Attempt 2: Comma-separated string
        try:
            # Filter out empty strings that can result from split (e.g. "a,,b" or "" or ", ")
            return [item_caster(item.strip()) for item in v.split(',') if item.strip()]
        except Exception as e: # Catch errors from item_caster or strip
            raise ValueError(f"Field '{field_name}': Cannot parse '{v}' as comma-separated list of {item_caster.__name__}s. Error: {e}")

    @field_validator('vector', mode='before')
    @classmethod
    def validate_vector(cls, v: Any, info: ValidationInfo) -> Any:
        if isinstance(v, list):
            try: # Ensure all items in an existing list are castable to float
                return [float(item) for item in v]
            except (TypeError, ValueError) as e:
                raise ValueError(f"Field '{info.field_name}': Supplied list contains non-numeric values. Error: {e}")
        # If a string, parse it using the helper. Otherwise, Pydantic handles (e.g. None for Optional, or wrong type)
        return cls._parse_string_to_list(v, float, info.field_name)

    @field_validator('keywords', mode='before')
    @classmethod
    def validate_keywords(cls, v: Any, info: ValidationInfo) -> Any:
        return ast.literal_eval(v)  
