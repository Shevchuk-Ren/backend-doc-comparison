from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schema import UserCreate, UserRead
from app.utils import auth
from app.db.models.user_model import User


class UserService:
    async def create_user(self, user: UserCreate, db: AsyncSession) -> UserRead:
        result = await db.execute(select(User).where(User.username == user.username))
        db_user = result.scalar_one_or_none()

        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        # Create new user
        hashed_password = auth.get_password_hash(user.password)
        new_user = User(username=user.username, hashed_password=hashed_password)

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return UserRead(
            id=new_user.id, username=new_user.username, created_at=new_user.created_at
        )
