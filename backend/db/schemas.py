from pydantic import BaseModel
from datetime import datetime

class EmployeeCreate(BaseModel):
    name:str
    phone:str
    dept_id:int
    role_id:int