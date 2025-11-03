from fastapi import APIRouter, Depends
from backend.db.models import Employee
from backend.db.database import get_db
from sqlalchemy.orm import Session
from backend.db.schemas import EmployeeCreate
from backend.db.crud import create_employee,fetch_emp_by_id,delete_employee
employeeRouter = APIRouter(
    prefix = "/employees",
    tags = ["Employees"]
)

@employeeRouter.get('/')
def hello():
    return "hello from employee API"

@employeeRouter.get('/{empid}')
def get_employee_details(empid:int,db:Session=Depends(get_db)):
    employee = fetch_emp_by_id(empid,db)
    if not employee:
        return {"statusCode":404,"message":"Employee not found!"}
    return {"statusCode":200,"message":f"employee:{employee}"}

@employeeRouter.post('/create')
def create_new_employee(emp: EmployeeCreate,db:Session=Depends(get_db)):
    if db.query(Employee).filter(emp.phone == Employee.id).first():
        return {"statusCode":409,"message":"Employee already exists with the specified number"}
    if create_employee(emp,db):
        return {"statusCode":201,"message":"Employee created"}
    else:
        return {"statusCode":400,"message":"Couldnt complete the request"}

@employeeRouter.post('/delete/{empid}')
def delete_employee_record(empid:int,db:Session=Depends(get_db)):
    if delete_employee(empid,db):
        return {"statusCode":200,"message":"Employee deleted from database"}
    else:
        return {"statusCode":400,"message":"Couldnt complete the request"}