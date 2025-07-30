from sqlalchemy import Column, Integer, String,Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum
from aetherml_settings.model.entity.base import Base


class UserRole(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    BROKER = "broker"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True)

    properties = relationship("Property", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.value}')>"


    