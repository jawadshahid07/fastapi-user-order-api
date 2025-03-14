from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=dict)
def create_order(request: Request, order_data: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order for the logged-in customer."""
    
    # Ensure user is authenticated
    if not hasattr(request.state, "user") or not request.state.user:
        raise HTTPException(status_code=401, detail="Authentication required")

    user = request.state.user  # Authenticated user

    # Create new order
    new_order = Order(
        user_id=user.id,
        total_amount=order_data.total_amount,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {"message": "Order created successfully", "order_id": new_order.id}

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, request: Request, db: Session = Depends(get_db)):
    """Retrieve order details by ID."""
    
    # Ensure user is authenticated
    if not hasattr(request.state, "user") or not request.state.user:
        raise HTTPException(status_code=401, detail="Authentication required")

    user = request.state.user  # Authenticated user

    # Fetch order from DB
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Only allow access if user is Admin or owns the order
    if user.role != "admin" and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return order
