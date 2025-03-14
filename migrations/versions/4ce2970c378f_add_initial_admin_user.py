"""Add initial admin user

Revision ID: 4ce2970c378f
Revises: cac8054cb966
Create Date: 2025-03-14 10:49:19.837899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import text
from app.db.database import engine
from passlib.context import CryptContext

# revision identifiers, used by Alembic.
revision: str = '4ce2970c378f'
down_revision: Union[str, None] = 'cac8054cb966'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def upgrade():
    """Add an initial admin user to the users table."""
    hashed_password = pwd_context.hash("admin123")  # Set a secure password
    
    conn = engine.connect()
    conn.execute(
        text(
            "INSERT INTO users (username, email, hashed_password, role) "
            "VALUES (:username, :email, :password, :role)"
        ),
        {
            "username": "admin",
            "email": "admin@example.com",
            "password": hashed_password,
            "role": "admin"
        }
    )
    conn.commit()
    conn.close()

def downgrade():
    """Remove the initial admin user if the migration is rolled back."""
    conn = engine.connect()
    conn.execute(text("DELETE FROM users WHERE username = 'admin'"))
    conn.commit()
    conn.close()