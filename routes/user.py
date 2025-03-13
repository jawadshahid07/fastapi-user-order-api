from fastapi import APIRouter, Depends
from ..auth import get_current_user
from ..models import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_profile(user: User = Depends(get_current_user)):
    """Get current logged-in user profile."""
    return {"id": user.id, "username": user.username, "email": user.email, "role": user.role}