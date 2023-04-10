from fastapi import APIRouter, Depends
from schemas.triangle import TriangleRequest
from sqlalchemy.orm import Session
from core.responses import (
    common_response,
    InternalServerError,
)
from repository.user import UserRepository
from repository.logs import LogsRepository
from models import get_db_sync
from core.jwt import oauth2_scheme

router = APIRouter(prefix="", tags=["Triangle"])


def triangle_pattern(n):
    text = ""
    k = n - 1
    for i in range(0, n):
        for j in range(0, k):
            text += " "
        k -= 1
        for j in range(0, i + 1):
            if i % 2 != 0:
                text += "# "
            else:
                text += "* "

        text += "\n"

    return text


@router.post("/")
async def triangle(
    request: TriangleRequest,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme),
):
    try:
        request_user = UserRepository.get_user_from_jwt_token(db=db, jwt_token=token)

        # create log
        LogsRepository.create_log(db=db, user_id=request_user.id, row=request.row)

        result = triangle_pattern(n=request.row)
        return result
    except Exception as e:
        return common_response(InternalServerError(error=str(e)))
