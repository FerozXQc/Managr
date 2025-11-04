from pydantic import BaseModel
from datetime import datetime

class CreateEmployeeSchema(BaseModel):
    name:str
    phone:str
    dept_id:int
    role_id:int

class CreateDepartmentSchema(BaseModel):
    dept:str
    description:str