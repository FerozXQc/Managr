from pydantic import BaseModel,Field
from datetime import date

class CreateEmployeeSchema(BaseModel):
    name:str
    phone:str
    department_id:int
    role_id:int

class CreateDepartmentSchema(BaseModel):
    department:str
    description:str

class EmployeeIdSchema(BaseModel):
    employee_id:int

class AttendanceDateRangeSchema(BaseModel):
    employee_id:int
    from_date:date
    to_date:date

class AttendanceMonthRangeSchema(BaseModel):
    employee_id:int
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$")  # YYYY-MM

