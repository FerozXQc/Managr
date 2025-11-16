from backend.db.models import (EmployeeDetails)
from backend.db.schemas import CreateEmployeeSchema
from sqlalchemy.orm import Session
from sqlalchemy import select

def fetch_emp_by_id(employee_id:int,db:Session):
    user = db.query(EmployeeDetails).filter(EmployeeDetails.employee_id == employee_id).first()
    # print(user)
    return user

def fetch_emp_by_email(email,db:Session):
    return db.query(EmployeeDetails).filter(EmployeeDetails.email == email).first()

# def create_employee(CreateEmployeeSchema, db: Session):
#     emp = EmployeeDetails(**CreateEmployeeSchema.dict())
#     try:
#         db.add(emp)
#         db.commit()
#         db.refresh(emp)
#         return emp
#     except Exception as e:
#         db.rollback()
#         print(f"Error creating employee: {e}")
#         return None

def delete_employee(employee_id: int, db: Session):
    user = fetch_emp_by_id(employee_id, db)
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

