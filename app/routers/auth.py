from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from app.database import get_db

# from app.schemas import AuthRequest
from app.models import Users
from app.utils import verify_password
from app.oauth2 import generate_access_token


router = APIRouter(prefix="/login", tags=["Authentication"])

# OAuth2PasswordRequestForm = Depends()
@router.post("/")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(Users).filter(Users.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    v = verify_password(request.password, user.password)
    if not v:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    token = generate_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
