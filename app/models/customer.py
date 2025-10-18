import uuid
from sqlalchemy import Column, String, Integer
from app.models import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    google_id = Column(String(255), unique=True, nullable=False)
    age = Column(Integer, nullable=True)
