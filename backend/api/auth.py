# backend/routers/auth.py
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import uuid
import os
from dotenv import load_dotenv

import jwt
from jwt.exceptions import ExpiredSignatureError, PyJWTError

from backend.db.database import get_db
from backend.db.models import Employee, UserRole
from backend.services.employee_service import fetch_emp_by_email
from backend.services.auth_service import authenticate_employee

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")                  
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", SECRET_KEY)

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY missing in .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

authRouter = APIRouter(prefix="/auth", tags=["Authentication"])



def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "jti": str(uuid.uuid4())
    })
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)



async def get_current_user(
    access_token: Annotated[Optional[str], Cookie(alias="access_token")] = None,
    db: Session = Depends(get_db)
) -> Employee:
    if not access_token or not access_token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = access_token.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        token_type: str = payload.get("type")
        if not email or token_type != "access":
            raise HTTPException(status_code=401, detail="Invalid access token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = fetch_emp_by_email(email, db)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

def require_super_admin(user: Employee = Depends(get_current_user)):
    if user.auth_role != UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Super admin privileges required")
    return user


@authRouter.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db: Session = Depends(get_db)
):
    user = authenticate_employee(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token({"sub": user.email, "role": user.auth_role})
    refresh_token = create_refresh_token({"sub": user.email})

    # Set HttpOnly cookies
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,          
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        path="/auth",
    )

    # Update last login
    user.last_login_at = datetime.now(timezone.utc)
    db.commit()

    return {"message": "Login successful"}


@authRouter.post("/refresh")
async def refresh_token_endpoint(
    response: Response,
    refresh_token: Annotated[Optional[str], Cookie(alias="refresh_token")] = None,
    db: Session = Depends(get_db)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        if not email or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = fetch_emp_by_email(email, db)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    new_access_token = create_access_token({"sub": user.email, "role": user.auth_role.value})

    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_access_token}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )

    return {"message": "Token refreshed"}


@authRouter.get("/me")
async def read_current_user(user: Employee = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "auth_role": user.auth_role.value,
        "is_active": user.is_active
    }


@authRouter.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token", path="/", httponly=True)
    response.delete_cookie(key="refresh_token", path="/auth", httponly=True)
    return {"message": "Logged out successfully"}