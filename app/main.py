from fastapi import FastAPI
from app.auth.middleware import AuthMiddleware
from app.routes import auth, users
from app.db.database import engine, Base

app = FastAPI()

# Create database tables (if not created)
Base.metadata.create_all(bind=engine)

# Register middleware
app.add_middleware(AuthMiddleware)

# Register routes
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "FastAPI is running!"}