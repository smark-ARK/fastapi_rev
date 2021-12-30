from datetime import datetime, timedelta
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from starlette import status

from app.database import get_db
from app.models import Users
from app.env_validate import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
ACCESS_EXPIRE_MINUTES = settings.ACCESS_EXPIRE_MINUTES


def generate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token, credential_exception):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = token_data.get("user_id")
        if id == None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return id


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-AUTENTICATE": "BEARER"},
    )
    id = verify_access_token(token, credential_exception)
    user = db.query(Users).filter(id == Users.id).first()
    return user
