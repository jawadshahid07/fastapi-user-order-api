from fastapi import FastAPI
from database import engine, Base
from routes import auth, users

app = FastAPI()

# Create database tables (if not created)
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(auth.router)
app.include_router(users.router)
