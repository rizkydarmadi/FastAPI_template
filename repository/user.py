from sqlalchemy.orm import Session
from typing import Optional
from models.user import User
import bcrypt
from sqlalchemy import select
from datetime import datetime, timedelta
from pytz import timezone
from jose import JWTError, jwt
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, TZ


class UserRepository:
    def generate_hash_password(password: str) -> str:
        hash = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        return hash.decode()

    def validated_user_password(hash: str, password: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode(), hash.encode())
        except:  # noqa: E722
            return False

    def get_user_name(db: Session, username: str) -> Optional[User]:
        user = db.query(User).filter(User.username == username).first()
        if user == None:  # noqa: E711
            return False
        return user

    def check_user_password(db: Session, username: str, password: str):
        user = UserRepository.get_user_name(db=db, username=username)

        return UserRepository.validated_user_password(user.password, password)

    async def generate_jwt_token_from_user(
        user: User, ignore_timezone: bool = False
    ) -> str:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        if ignore_timezone == False:  # For testing  # noqa: E712
            expire = expire.astimezone(timezone(TZ))
        payload = {
            "id": str(user.id),
            "username": user.email,
            "email": user.email,
            "exp": expire,
        }
        jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return jwt_token

    def create(db: Session, username: str, password: str, email: str) -> Optional[User]:
        new_user = User(
            username=username,
            email=email,
            password=UserRepository.generate_hash_password(password),
        )
        db.add(new_user)
        db.commit()
        return new_user

    def get_user_from_jwt_token(db: Session, jwt_token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token=jwt_token, key=SECRET_KEY, algorithms=ALGORITHM)
            id = payload.get("id")
            query = select(User).filter(User.id == int(id))
            user = db.execute(query).scalar()
        except JWTError:
            return None

        return user
