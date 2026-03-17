from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import get_sesion
from app.schemas.user_schema import UserCreate, Token
from app.services.users_service import UserService

router = APIRouter(tags=["Auth"])
user_service = UserService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


@router.post("/users/registration", summary="Create user")
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_sesion),
):
    return await user_service.create_user(payload, db)


@router.post("/users/token", summary="Get token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_sesion),
):
    return await user_service.login(form_data, db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_sesion),
):
    return await user_service.get_current_user(token, db)


@router.get("/users/me", summary="Get current user")
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user
