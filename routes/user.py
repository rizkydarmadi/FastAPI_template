from fastapi import APIRouter, Depends
from schemas.user import UserCreateRequest, UserCreateResponse, JwtResponse
from sqlalchemy.orm import Session
from schemas.common import (
    InternalServerErrorResponse,
)
from core.responses import (
    BadRequest,
    common_response,
    Created,
    InternalServerError,
)
from repository.user import UserRepository
from fastapi.security import OAuth2PasswordRequestForm
from models import get_db_sync
import traceback

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "/",
    responses={
        "200": {"model": UserCreateResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def create_user(request: UserCreateRequest, db: Session = Depends(get_db_sync)):
    try:
        new_user = UserRepository.create(
            db=db,
            username=request.username,
            password=request.password,
            email=request.email,
        )

        return common_response(
            Created(
                data={
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                }
            )
        )
    except Exception as e:
        return common_response(InternalServerError(error=str(e)))


@router.post(
    "/token/",
    responses={
        "200": {"model": JwtResponse},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def generate_token(
    db: Session = Depends(get_db_sync), form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        is_valid = UserRepository.check_user_password(
            db, form_data.username, form_data.password
        )
        if not is_valid:
            return common_response(BadRequest(message="Invalid Credentials"))
        user = UserRepository.get_user_name(db=db, username=form_data.username)
        token = await UserRepository.generate_jwt_token_from_user(user=user)
        return {"access_token": token, "token_type": "Bearer"}
    except Exception as e:
        traceback.print_exc()
        return common_response(InternalServerError(error=str(e)))
