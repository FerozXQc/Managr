from fastapi import APIRouter, Depends
from backend.db.models import Employee
from backend.db.database import get_db
from sqlalchemy.orm import Session
from backend.db.schemas import CreateEmployeeSchema
from backend.services.employee_service import create_employee,fetch_emp_by_id,delete_employee

employeeRouter = APIRouter(
    prefix = "/employees",
    tags = ["Employees"]
)

@employeeRouter.get('/{emp_id}')
def get_employee_details(emp_id:int,db:Session=Depends(get_db)):
    employee = fetch_emp_by_id(emp_id,db)
    if not employee:
        return {"statusCode":404,"message":"Employee not found!"}
    return {"statusCode":200,"message":f"employee:{employee}"}

@employeeRouter.post('/create')
def create_new_employee(emp: CreateEmployeeSchema,db:Session=Depends(get_db)):
    if db.query(Employee).filter(emp.phone == Employee.phone).first():
        return {"statusCode":409,"message":"Employee already exists with the specified number"}
    if create_employee(emp,db):
        return {"statusCode":201,"message":"Employee created"}
    else:
        return {"statusCode":400,"message":"Couldnt complete the request"}

@employeeRouter.post('/delete/{emp_id}')
def delete_employee_record(emp_id:int,db:Session=Depends(get_db)):
    if not fetch_emp_by_id(emp_id,db):
        return {"statusCode":404,"message":"Employee not found!"}
    if delete_employee(emp_id,db):
        return {"statusCode":200,"message":"Employee deleted from database"}
    else:
        return {"statusCode":400,"message":"Couldnt complete the request"}
