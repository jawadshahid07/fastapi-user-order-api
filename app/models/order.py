from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.models import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    order_date = Column(TIMESTAMP, server_default=func.now())
    total_amount = Column(DECIMAL, nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
