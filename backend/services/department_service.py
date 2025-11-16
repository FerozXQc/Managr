from backend.db.models import (EmployeeDetails,Department,Role,Attendance)
from backend.db.schemas import CreateDepartmentSchema
from sqlalchemy.orm import Session

def fetch_dept_by_id(department_id:int,db:Session):
    return db.query(Department).filter(Department.id == department_id).first()

def fetch_emp_by_dept(department_id: int, db: Session):
    #returns [] if no records found
    return db.query(EmployeeDetails).filter(EmployeeDetails.department_id == department_id).all()

def create_department(department: CreateDepartmentSchema, db:Session):
    department_record = Department(**department.dict())

    try:
        db.add(department_record)
        db.commit()
        db.refresh(department_record)
        return department_record
    except Exception as e:
        db.rollback()
        print(f"Error creating employee: {e}")
        return None

def delete_department(department_id: int, db: Session):
    department = fetch_dept_by_id(department_id, db)
    if not department:
        return None
    try:
        db.delete(department)
        db.commit()
        return department
    except Exception as e:
        db.rollback()
        print(f"Error deleting employee: {e}")
        return None
