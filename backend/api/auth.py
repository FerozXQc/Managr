from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session = Depends(get_db)
) -> Token:
    user = authenticate_employee(form_data.username,form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



