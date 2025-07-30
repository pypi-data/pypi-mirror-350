from pydantic import BaseModel, EmailStr
from typing import Optional
import enum

# Mirror the SQLAlchemy UserRole enum
class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    BROKER = "broker"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.CUSTOMER

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    # properties: List['Property'] = [] # Forward reference for Property DTO

    class Config:
        from_attributes = True # Changed from orm_mode = True

# Forward reference update for Property DTO
# Needs to be done after Property DTO is defined
# Or handled by importing Property DTO and using it directly
# For now, commenting out to avoid circular dependency if Property DTO imports User 