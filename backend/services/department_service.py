from backend.db.models import (Employee,Department,Role,Attendance)
from backend.db.schemas import CreateDepartmentSchema
from sqlalchemy.orm import Session

def fetch_dept_by_id(dept_id:int,db:Session):
    return db.query(Department).filter(Department.id == dept_id).first()

def fetch_emp_by_dept(dept_id: int, db: Session):
    #returns [] if no records found
    return db.query(Employee).filter(Employee.dept_id == dept_id).all()

def create_department(dept: CreateDepartmentSchema, db:Session):
    dept_record = Department(**dept.dict())

    try:
        db.add(dept_record)
        db.commit()
        db.refresh(dept_record)
        return dept_record
    except Exception as e:
        db.rollback()
        print(f"Error creating employee: {e}")
        return None

def delete_department(dept_id: int, db: Session):
    dept = fetch_dept_by_id(dept_id, db)
    if not dept:
        return None
    try:
        db.delete(dept)
        db.commit()
        return dept
    except Exception as e:
        db.rollback()
        print(f"Error deleting employee: {e}")
        return None
