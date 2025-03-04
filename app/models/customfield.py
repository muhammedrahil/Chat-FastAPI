import enum
from sqlalchemy import Column,UUID, Float, ForeignKey, Index, Integer, String, Text
from app.db.database import Base
import uuid
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True,default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    profile_image = Column(String, nullable=True)  # Store image URL or file path



class FieldType(enum.Enum):
    TEXT = "text"
    NUMBER = "number"
    EMAIL = "email"
    PHONE = "phone"
    AMOUNT = "amount"
    TEXT_AREA = "textarea"
    DROP_DOWN = "dropdown"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    DATE = "date"
    TIME = "time"
    FILE = "file"
    IMAGE = "image"

class CustomField(Base):
    __tablename__ = "customfields"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)  # Field label
    field_type = Column(enum.Enum(FieldType), nullable=False)  # Type of field
    required = Column(Integer, default=0)  # 1 = Required, 0 = Optional
    model_name = Column(String, nullable=False, index=True)  # Which table uses this field

    min_length = Column(Integer, nullable=True)  # Min length for text fields
    max_length = Column(Integer, nullable=True)  # Max length for text fields
    regex = Column(String, nullable=True)  # Regex pattern (e.g., email, phone)
    min_value = Column(Float, nullable=True)  # Min value for number fields
    max_value = Column(Float, nullable=True)  # Max value for number fields
    
    options = relationship("CustomFieldOption", back_populates="field")

class CustomFieldOption(Base):
    __tablename__ = "customfield_options"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("customfields.id", ondelete="CASCADE"))
    option_value = Column(String, nullable=False)  # Option value (e.g., "Male", "Female")

    field = relationship("CustomField", back_populates="options")

class CustomFieldValue(Base):
    __tablename__ = "customfield_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("customfields.id", ondelete="CASCADE"))
    object_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # The ID of the record (User, Order, etc.)
    model_name = Column(String, nullable=False, index=True)  # Which table this value belongs to
    value = Column(Text, nullable=True)  # Stores field value as text

    field = relationship("CustomField")