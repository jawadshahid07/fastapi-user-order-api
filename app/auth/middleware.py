from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.auth.auth import decode_access_token
from app.models.user import User

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to extract and verify JWT token from requests."""

    async def dispatch(self, request: Request, call_next):
        """Intercepts incoming requests to verify JWT authentication."""

        # Bypass authentication for public routes
        public_routes = {"/", "/auth/login", "/auth/register", "/docs", "/openapi.json"}
        if request.url.path in public_routes:
            return await call_next(request)

        # Get Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")

        # Extract token
        token = auth_header.split("Bearer ")[1]

        try:
            # Decode token
            payload = decode_access_token(token)
            if not payload or "sub" not in payload:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            user_id = payload["sub"]
            if not isinstance(user_id, int):  # Convert sub to integer if needed
                try:
                    user_id = int(user_id)
                except ValueError:
                    raise HTTPException(status_code=401, detail="Invalid user ID in token")

            # Attach user to request state
            db: Session = next(get_db())  # Get database session
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                raise HTTPException(status_code=401, detail="User not found")

            request.state.user = user  # Store user in request state
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status_code=401, detail="Token verification failed")

        return await call_next(request)
