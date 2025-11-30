from fastapi import APIRouter, Depends
from backend.db.models import Department
from backend.db.database import get_db
from sqlalchemy.orm import Session
from backend.db.schemas import CreateEmployeeSchema, CreateDepartmentSchema
from backend.services.department_service import create_department,fetch_dept_by_id,fetch_emp_by_dept,delete_department 

departmentRouter = APIRouter(
    prefix = "/departments",
    tags = ["Departments"]
)

@departmentRouter.get('/{department_id}')
def get_department_details(department_id:int,db:Session=Depends(get_db)):
    department = fetch_dept_by_id(department_id,db)
    if not department:
        return {"statusCode":404,"message":"Department not found!"}
    return {"statusCode":200,"department":department}

@departmentRouter.post('/create')
def create_new_department(department: CreateDepartmentSchema,db:Session=Depends(get_db)):
    if db.query(Department).filter(Department.name == department.name).first():
        return {"statusCode":409,"message":"Department already exists with the specified name"}
    if create_department(department,db):
        return {"statusCode":201,"message":"Department created"}

    else:
        return {"statusCode":400,"message":"Couldnt complete the request"}

@departmentRouter.get("/{department_id}/employees")
def get_employees_by_department(department_id:int,db:Session=Depends(get_db)):
    if not db.query(Department).filter(Department.id == department_id).first():
        return {"statusCode":404,"message":f"Department with the id {department_id} not found!"}
    employees = fetch_emp_by_dept(department_id,db)
    if employees == []:
        return {"statusCode":404,"message":f"No employee found"}
    return {"statusCode":200,"employees":employees}

@departmentRouter.delete('/delete/{dept_id}')
def delete_employee_record(dept_id:int,db:Session=Depends(get_db)):
    if not fetch_dept_by_id(dept_id,db):
        return {"statusCode":404,"message":"Department not found!"}
    if delete_department(dept_id,db):
        return {"statusCode":200,"message":"Department deleted from database"}
    else:
        return {"statusCode":400,"message":"Couldnt complete the request"}