import uuid
from sqlalchemy import Column, String, Enum, Numeric, DateTime
from sqlalchemy.sql import func
import enum
from app.models import Base


class PaymentStatusEnum(str, enum.Enum):
    pass_status = "pass"
    fail = "fail"


class PaymentTypeEnum(str, enum.Enum):
    upi = "UPI"
    card = "card"


class Payment(Base):
    __tablename__ = "payments"
    transaction_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(Enum(PaymentStatusEnum), nullable=False)
    payment_type = Column(Enum(PaymentTypeEnum), nullable=False)
    amount = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())