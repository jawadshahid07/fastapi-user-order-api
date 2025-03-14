from pydantic import BaseModel, EmailStr

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