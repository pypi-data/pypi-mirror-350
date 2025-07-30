from pydantic import BaseModel, field_validator, ValidationInfo
from typing import Optional, List, Any, Union
from aetherml_settings.model.dto.user_dto import User


class PropertyBase(BaseModel):
    operation: str
    price: float
    state: str
    city: str
    area: str
    address: str # how to vaidate if it is a real address?
    name: str
    title: str
    company: Optional[str] = None
    image: str
    phone: Optional[str] = None
    email: Optional[str] = None
    experience: Optional[int] = None
    activeListings: Optional[int] = None
    amenities: Optional[Union[str, Any]] = None # Or List[str] depending on JSON structure
    bedrooms: int = None
    bathrooms: float = None
    constructionSize: float 
    lotSize: Optional[float] = None
    parking: Optional[int] = None
    floors: Optional[int] = None
    property_type: str = None
    type: Optional[str] = None
    latitude: float
    longitude: float
    description: Optional[str] = None
    user_id: int # For linking to the owner

    @field_validator('bathrooms', 'bedrooms', mode='before')
    def validate_bathrooms_bedrooms(cls, v, info: ValidationInfo):
        if v is not None and v < 0:
            raise ValueError(f"{info.field_name} cannot be negative")
        return v

    @field_validator('constructionSize', 'lotSize', mode='before')
    def validate_construction_size(cls, v, info: ValidationInfo):
        if v is not None and v < 0:
            raise ValueError(f"{info.field_name} cannot be negative")
        return v

class PropertyDTO(PropertyBase):
    # Add any fields that are required on creation and not optional
    # For example, if title and address are always required:
    title: str
    address: str
    price: float
    # user_id will be set by the application based on the authenticated user

class PropertyUpdate(PropertyBase):
    # All fields are optional by default in PropertyBase
    pass

class Property(PropertyBase):
    id: int
    # owner: Optional['User'] = None # Forward reference for User DTO

    class Config:
        from_attributes = True # Changed from orm_mode = True


class ComposeProperty(BaseModel):
    property: Property
    user: User

class ComposePropertyList(BaseModel):
    properties: List[ComposeProperty]

# To handle the forward reference 'User', you would typically import User DTO:
# from .user_dto import User 
# And then update the Property model:
# Property.model_rebuild() # Pydantic v2
# or Property.update_forward_refs() # Pydantic v1 