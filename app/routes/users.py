from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.auth.auth import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

# Define response model
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

@router.get("/me", response_model=UserResponse)
def get_profile(request: Request):
    """Get current logged-in user profile. Only accessible by customers."""

    # Ensure request.state.user is set by middleware
    if not hasattr(request.state, "user") or not request.state.user:
        raise HTTPException(status_code=401, detail="Authentication failed")

    user = request.state.user

    # Ensure the user is a customer
    if user.role != "customer":
        raise HTTPException(status_code=403, detail="Only customers can access this route")

    return user  # FastAPI automatically converts SQLAlchemy model to Pydantic


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

@router.post("/", status_code=201)
def create_user(request: Request, user_data: CreateUserRequest, db: Session = Depends(get_db)):
    """Create a new user. Only Admins can access this API."""
    
    # Ensure request.state.user is set by middleware
    if not hasattr(request.state, "user") or not request.state.user:
        raise HTTPException(status_code=401, detail="Authentication required")

    logged_in_user = request.state.user

    # Ensure only admins can access this API
    if logged_in_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create users")

    # Check if the email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password and create user
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw,
        role = user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "id": new_user.id}
