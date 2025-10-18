import uuid
from sqlalchemy import Column, String, Enum
import enum
from app.models import Base


class AreaEnum(str, enum.Enum):
    mumbai = "Mumbai"
    bangalore = "Bangalore"


class Restaurant(Base):
    __tablename__ = "restaurants"
    restaurant_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_name = Column(String(255), nullable=False)
    area = Column(Enum(AreaEnum), nullable=False)