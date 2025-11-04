from backend.db.models import (Employee)
from backend.db.schemas import CreateEmployeeSchema
from sqlalchemy.orm import Session

def fetch_emp_by_id(empid:int,db:Session):
    user = db.query(Employee).filter(Employee.id == empid).first()
    # print(user)
    return user

def create_employee(EmployeeCreate, db: Session):
    emp = Employee(**EmployeeCreate.dict())
    try:
        db.add(emp)
        db.commit()
        db.refresh(emp)
        return emp
    except Exception as e:
        db.rollback()
        print(f"Error creating employee: {e}")
        return None

def delete_employee(emp_id: int, db: Session):
    user = fetch_emp_by_id(emp_id, db)
    if not user:
        return None
    try:
        db.delete(user)
        db.commit()
        return user
    except Exception as e:
        db.rollback()
        print(f"Error deleting employee: {e}")
        return None

