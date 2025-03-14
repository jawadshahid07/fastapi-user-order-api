from sqlalchemy.orm import declarative_base

Base = declarative_base()  # Define Base here

# Import models after defining Base
from app.models.user import User
from app.models.order import Order

__all__ = ["Base", "User", "Order"]  # Helps avoid import issues
