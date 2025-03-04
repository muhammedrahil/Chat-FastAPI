from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4

class UserResponse(BaseModel):
    id: UUID4
    name: str
    email: EmailStr
    profile_image: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    profile_image: Optional[str] = None