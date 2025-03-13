from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from database import get_db
from auth import decode_access_token
from models import User

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to extract and verify JWT token from requests."""

    async def dispatch(self, request: Request, call_next):
        """Intercepts incoming requests to verify JWT authentication."""

        # Bypass authentication for public routes
        public_routes = ["/auth/login", "/auth/register", "/docs", "/openapi.json"]
        if any(request.url.path.startswith(route) for route in public_routes):
            return await call_next(request)

        # Get the Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")

        # Extract the token
        token = auth_header.split("Bearer ")[1]

        try:
            payload = decode_access_token(token)

            if not payload or "sub" not in payload:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            user_id = payload["sub"]
            if not isinstance(user_id, int):  # Convert sub to integer if it's a string
                try:
                    user_id = int(user_id)
                except ValueError:
                    raise HTTPException(status_code=401, detail="Invalid user ID in token")

            # Attach the user to the request state
            db: Session = next(get_db())  # Get a database session
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                raise HTTPException(status_code=401, detail="User not found")

            request.state.user = user  # Store user in request state
        except HTTPException as e:
            raise e  # Raise existing HTTP exceptions (e.g., expired token)
        except Exception as e:
            raise HTTPException(status_code=401, detail="Token verification failed")

        return await call_next(request)  # Proceed to the actual API
