from typing import List
from fastapi import APIRouter, Depends, status,HTTPException
from app.schemas.customfield import UserResponse, UserCreate
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.customfield import User
from sqlalchemy import select

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    return users


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # Refresh to get latest state

    return new_user