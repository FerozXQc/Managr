# backend/app/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .db import test_model
# 1️⃣ Base & Engine setup first
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///managr.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2️⃣ Import models *after* Base is defined


# 3️⃣ Create tables
Base.metadata.create_all(bind=engine)
