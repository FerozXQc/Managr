from .database import get_db, engine, Base
from . import models

Base.metadata.create_all(bind=engine)
print('tables created')
__all__ = ["get_db", "engine", "Base"]
