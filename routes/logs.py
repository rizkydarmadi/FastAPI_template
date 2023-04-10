from fastapi import APIRouter, Depends
from schemas.logs import GetAllResponse
from schemas.common import (
    InternalServerErrorResponse,
)
from sqlalchemy.orm import Session
from core.responses import (
    common_response,
    Created,
    InternalServerError,
)
from repository.logs import LogsRepository
from models import get_db_sync
from core.jwt import oauth2_scheme
from typing import List

router = APIRouter(prefix="/log", tags=["Logs"])


@router.get(
    "/",
    responses={
        "200": {"model": List[GetAllResponse]},
        "500": {"model": InternalServerErrorResponse},
    },
)
async def get_all_log(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db_sync),
    token: str = Depends(oauth2_scheme),
):
    try:
        data = LogsRepository.get_all_logs(page=page, limit=limit, db=db)

        return common_response(
            Created(
                data=[
                    {
                        "user": i.user.username,
                        "row": i.row_input,
                        "date": i.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    for i in data
                ]
            )
        )
    except Exception as e:
        return common_response(InternalServerError(error=str(e)))
