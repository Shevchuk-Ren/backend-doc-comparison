import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user_schema import UserCreate
from app.services.users_service import UserService
from app.utils import auth
from tests.factories import UserFactory


@pytest.mark.asyncio
async def test_create_user_success(db_session):
    service = UserService()
    payload = UserCreate(username="alice", password="secret123")

    result = await service.create_user(payload, db_session)

    assert result.username == "alice"
    assert result.id is not None
    assert result.created_at is not None


@pytest.mark.asyncio
async def test_create_user_duplicate_username(db_session):
    service = UserService()

    existing_user = UserFactory.build(
        username="alice",
        hashed_password=auth.get_password_hash("secret123"),
    )
    db_session.add(existing_user)
    await db_session.commit()

    payload = UserCreate(username="alice", password="anotherpass")

    with pytest.raises(HTTPException) as exc:
        await service.create_user(payload, db_session)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Username already registered"


@pytest.mark.asyncio
async def test_login_success(db_session):
    service = UserService()

    user = UserFactory.build(
        username="alice",
        hashed_password=auth.get_password_hash("secret123"),
    )
    db_session.add(user)
    await db_session.commit()

    form_data = OAuth2PasswordRequestForm(
        username="alice",
        password="secret123",
        scope="",
        client_id=None,
        client_secret=None,
    )

    result = await service.login(form_data, db_session)

    assert "access_token" in result
    assert result["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(db_session):
    service = UserService()

    user = UserFactory.build(
        username="alice",
        hashed_password=auth.get_password_hash("secret123"),
    )
    db_session.add(user)
    await db_session.commit()

    form_data = OAuth2PasswordRequestForm(
        username="alice",
        password="wrong-password",
        scope="",
        client_id=None,
        client_secret=None,
    )

    with pytest.raises(HTTPException) as exc:
        await service.login(form_data, db_session)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Incorrect username or password"


@pytest.mark.asyncio
async def test_login_unknown_user(db_session):
    service = UserService()

    form_data = OAuth2PasswordRequestForm(
        username="ghost",
        password="secret123",
        scope="",
        client_id=None,
        client_secret=None,
    )

    with pytest.raises(HTTPException) as exc:
        await service.login(form_data, db_session)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Incorrect username or password"


@pytest.mark.asyncio
async def test_get_current_user_success(db_session):
    service = UserService()

    user = UserFactory.build(
        username="alice",
        hashed_password=auth.get_password_hash("secret123"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    token = auth.create_access_token(data={"sub": user.username})

    result = await service.get_current_user(token, db_session)

    assert result.id == user.id
    assert result.username == "alice"


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(db_session):
    service = UserService()

    with pytest.raises(HTTPException) as exc:
        await service.get_current_user("broken-token", db_session)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid authentication credentials"


@pytest.mark.asyncio
async def test_get_current_user_user_not_found(db_session):
    service = UserService()

    token = auth.create_access_token(data={"sub": "missing_user"})

    with pytest.raises(HTTPException) as exc:
        await service.get_current_user(token, db_session)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"
