from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user_model import User
from app.schemas.user_schema import UserCreate, UserRead
from app.utils import auth


class UserService:
    async def create_user(self, user: UserCreate, db: AsyncSession) -> UserRead:
        result = await db.execute(select(User).where(User.username == user.username))
        db_user = result.scalar_one_or_none()

        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        hashed_password = auth.get_password_hash(user.password)
        new_user = User(username=user.username, hashed_password=hashed_password)

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return UserRead(
            id=new_user.id,
            username=new_user.username,
            created_at=new_user.created_at,
        )

    async def login(
        self,
        form_data: OAuth2PasswordRequestForm,
        db: AsyncSession,
    ) -> dict:
        result = await db.execute(
            select(User).where(User.username == form_data.username)
        )
        user = result.scalar_one_or_none()

        if not user or not auth.verify_password(
            form_data.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = auth.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_current_user(self, token: str, db: AsyncSession):
        username = auth.verify_token(token)

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return UserRead(
            id=user.id,
            username=user.username,
            created_at=user.created_at,
        )
