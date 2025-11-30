from pydantic import BaseModel,Field,EmailStr
from datetime import date

class VerifyEmployeeSchema(BaseModel):
    full_name:str
    email:str
    password:str

class AuthenticateEmployeeSchema(BaseModel):
    email:str
    password:str

class RegisterEmployeeSchema(BaseModel):
    full_name:str
    email:str
    password:str

class CreateEmployeeSchema(BaseModel):
    full_name:str
    email:str
    department_id:int
    role_id:int

class CreateDepartmentSchema(BaseModel):
    name:str
    description:str

class EmployeeIdSchema(BaseModel):
    id:int

class AttendanceDateRangeSchema(BaseModel):
    employee_details_id:int
    from_date:date
    to_date:date

class AttendanceMonthRangeSchema(BaseModel):
    employee_details_id:int
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$")  # YYYY-MM

class Token(BaseModel):
    access_token: str
    token_type: str

