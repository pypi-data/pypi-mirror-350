from sqlalchemy import Column, Integer, String, Float, Text, JSON, ForeignKey

from sqlalchemy.orm import relationship
from aetherml_settings.model.entity.base import Base
from aetherml_settings.model.entity.users import User


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    operation = Column(String, index=True)
    price = Column(Float)
    state = Column(String, index=True)
    city = Column(String, index=True)
    area = Column(String)  # e.g., neighborhood, district
    address = Column(String)
    name = Column(String)  # e.g., property name or contact person
    title = Column(String)  # Listing headline
    company = Column(String)  # Real estate agency
    image = Column(String)  # URL to main image
    phone = Column(String)
    email = Column(String)
    experience = Column(String)  # e.g., "5 years experience"
    activeListings = Column(Integer)  # Number of active listings for an agent/company
    amenities = Column(JSON)  # List of strings or key-value pairs
    bedrooms = Column(Integer)
    bathrooms = Column(Float)  # Allows for 0.5 bathrooms
    constructionSize = Column(Float)  # e.g., sq ft or sq m
    lotSize = Column(Float)  # e.g., sq ft or sq m
    parking = Column(Integer)  # Number of parking spots
    floors = Column(Integer)  # Number of floors
    property_type = Column(String, index=True)  # e.g., "Apartment", "House"
    type = Column(String)  # Could be further specified, e.g., "Residential", "Commercial"
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Added for User relationship
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="properties")
    
    description = Column(Text)

    # One-to-one relationship to ElasticPropertyEmbedding
    embedding = relationship(
        "ElasticPropertyEmbedding",  # String name is used here
        back_populates="property_record", 
        uselist=False, 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Property(id={self.id}, title='{self.title}', address='{self.address}')>"



