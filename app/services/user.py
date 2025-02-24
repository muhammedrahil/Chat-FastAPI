from app.models.user import User
from app.schemas.user import UserCreate
from app.db.session import SessionLocal

def create_user(user: UserCreate):
    db = SessionLocal()
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user
