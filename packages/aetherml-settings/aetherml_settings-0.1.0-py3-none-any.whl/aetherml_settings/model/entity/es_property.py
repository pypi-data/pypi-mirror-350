from aetherml_settings.model.entity.base import Base
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, FLOAT

import uuid

# Import Property for the relationship


class ElasticPropertyEmbedding(Base):
    """SQLAlchemy model representing the Elasticsearch property embedding mapping"""
    __tablename__ = 'elastic_property_embeddings'

    id = Column(Integer, primary_key=True)
    doc_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False)
    title = Column(Text)
    description = Column(Text)
    keywords = Column(JSON)
    vector = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    text = Column(Text)
    index_name = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    property_id = Column(Integer, ForeignKey("properties.id"), unique=True, nullable=False)

    property_record = relationship("Property", back_populates="embedding")