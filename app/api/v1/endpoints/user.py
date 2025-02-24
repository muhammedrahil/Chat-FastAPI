from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserResponse
from app.services.user import create_user

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate):
    return create_user(user)