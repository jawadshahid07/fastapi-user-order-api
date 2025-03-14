from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.auth.auth import hash_password
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

# Define response model
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

class UserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

class UpdateUserRequest(BaseModel):
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

@router.post("/", status_code=201)
def create_user(request: Request, user_data: UserRequest, db: Session = Depends(get_db)):
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

@router.get("/{user_id}")
def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    """Retrieve user details by ID. Admins can access any user, customers can only access their own profile."""
    
    # Ensure user is authenticated
    if not hasattr(request.state, "user") or not request.state.user:
        raise HTTPException(status_code=401, detail="Authentication required")

    logged_in_user = request.state.user

    # If not admin, ensure they are only requesting their own details
    if logged_in_user.role != "admin" and logged_in_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id, "username": user.username, "email": user.email, "role": user.role}

@router.put("/{user_id}")
def update_user(user_id: int, request: Request, user_data: UpdateUserRequest, db: Session = Depends(get_db)):
    """Update user details by ID. Admins can update any user, customers can only update their own profile."""
    
    # Ensure user is authenticated
    if not hasattr(request.state, "user") or not request.state.user:
        raise HTTPException(status_code=401, detail="Authentication required")

    logged_in_user = request.state.user

    # If not admin, ensure they are only updating their own details
    if logged_in_user.role != "admin" and logged_in_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields
    user.username = user_data.username
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return {"message": "User updated successfully", "id": user.id, "username": user.username, "email": user.email}

@router.delete("/{user_id}")
def delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    """Delete a user by ID (Admin only)."""

    # Ensure user is authenticated
    if not hasattr(request.state, "user") or not request.state.user:
        raise HTTPException(status_code=401, detail="Authentication required")

    logged_in_user = request.state.user

    # Only admins can delete users
    if logged_in_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete users")

    user = db.query(User).filter(User.id == user_id).first()
    
    # Ensure user exists
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Optional: Prevent admin from deleting themselves
    if logged_in_user.id == user.id:
        raise HTTPException(status_code=403, detail="Admins cannot delete themselves")

    db.delete(user)
    db.commit()

    return {"message": f"User {user.username} deleted successfully"}

@router.get("/", response_model=List[UserResponse])
def list_users(request: Request, db: Session = Depends(get_db)):
    """List all users (Admin only)."""

    # Ensure user is authenticated
    if not hasattr(request.state, "user") or not request.state.user:
        raise HTTPException(status_code=401, detail="Authentication required")

    logged_in_user = request.state.user

    # Only admins can list users
    if logged_in_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can list users")

    users = db.query(User).all()
    
    return users