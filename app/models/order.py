import uuid
from sqlalchemy import Column, String, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
import enum
from app.models import Base


class FoodItemEnum(str, enum.Enum):
    veg_manchurian = "veg manchurian"
    chicken_manchurian = "chicken manchurian"
    veg_fried_rice = "veg fried rice"
    chicken_noodles = "chicken noodles"


class Order(Base):
    __tablename__ = "orders"
    order_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    food_item = Column(Enum(FoodItemEnum), nullable=False)
    transaction_id = Column(String(36), ForeignKey("payments.transaction_id"), nullable=False)
    restaurant_id = Column(String(36), ForeignKey("restaurants.restaurant_id"), nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())