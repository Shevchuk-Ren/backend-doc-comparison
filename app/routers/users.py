from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserCreate
from app.db.postgres import get_sesion
from app.services.users_service import UserService
from sqlalchemy.orm import Session

router = APIRouter(tags=["Auth"])


user_service = UserService()


@router.post("/users/registration", summary="Create user")
async def create_user(payload: UserCreate, db: Session = Depends(get_sesion)):
    result = await user_service.create_user(payload, db)
    return result
