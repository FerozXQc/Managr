from typing import Annotated, Optional
from fastapi import Depends, APIRouter, HTTPException, status, Response,Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from backend.services.employee_service import fetch_emp_by_email
from backend.services.auth_service import authenticate_employee,register_employee
from backend.db.database import get_db
from sqlalchemy.orm import Session
from backend.db.schemas import AuthenticateEmployeeSchema, Token, RegisterEmployeeSchema
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
load_dotenv()
authRouter = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_employee(token: Annotated[str, Depends(oauth2_scheme)], db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    employee = fetch_emp_by_email(email,db)
    if employee is None:
        raise credentials_exception
    return employee

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


@authRouter.post('/register')
def register(employee: RegisterEmployeeSchema,db:Session=Depends(get_db)):
    if register_employee(employee,db):
        return {"statusCode":200, "message":f"employee created successfully"}
    else:
        return {"statusCode":409,"message":f'user already exists!'}


@authRouter.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db: Session = Depends(get_db),
):
    user = authenticate_employee(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,         
        samesite="lax",
        max_age=30 * 60,     
        path="/",
    )

    return {"message": "Login successful"}


async def get_current_user(access_token: Optional[str] = Cookie(default=None)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(access_token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM"))
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"email": email}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@authRouter.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return current_user 

@authRouter.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {"message": "Logged out successfully"}