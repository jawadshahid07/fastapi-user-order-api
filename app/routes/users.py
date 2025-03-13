from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/users", tags=["Users"])

# Define response model
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # Ensures SQLAlchemy objects are converted to Pydantic

@router.get("/me", response_model=UserResponse)
def get_profile(request: Request):
    """Get current logged-in user profile."""

    # Ensure request.state.user is set by middleware
    if not hasattr(request.state, "user") or not request.state.user:
        raise HTTPException(status_code=401, detail="Authentication failed")

    user = request.state.user

    # Ensure the user object is valid
    if not hasattr(user, "id") or not hasattr(user, "username") or not hasattr(user, "email"):
        raise HTTPException(status_code=401, detail="User not found")

    return user  # FastAPI automatically converts SQLAlchemy model to Pydantic
