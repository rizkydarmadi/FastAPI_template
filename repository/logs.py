from sqlalchemy.orm import Session
from typing import List
from models.log import Logs
from datetime import datetime


class LogsRepository:
    def get_all_logs(db: Session, limit: int, page: int) -> List[Logs]:
        offset = (page - 1) * limit
        result = db.query(Logs).limit(limit=limit).offset(offset=offset).all()
        return result

    def create_log(db: Session, user_id: int, row: int) -> None:
        new_log = Logs(user_id=user_id, row_input=row, created_date=datetime.now())
        db.add(new_log)
        db.commit()
