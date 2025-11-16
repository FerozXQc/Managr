from backend.db.models import Employee
from backend.utils.password import verify_password_hash,get_password_hash
# from backend.services.employee_service import fetch_emp_by_email
from backend.db.schemas import AuthenticateEmployeeSchema,RegisterEmployeeSchema
from sqlalchemy.orm import Session
import jwt

def fetch_emp_by_email(email,db:Session):
    return db.query(Employee).filter(Employee.email == email).first()


def authenticate_employee(email:str,password:str,db:Session):
    employee = fetch_emp_by_email(email,db)
    if not employee:
        return False
    if not verify_password_hash(plain_password=password,hashed_password=employee.password):
        return False
    return employee

def register_employee(schema:RegisterEmployeeSchema,db:Session):
    if fetch_emp_by_email(schema.email,db):
        return False
    schema.password = get_password_hash(schema.password)
    try:
        employee = Employee(**schema.dict())
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    except Exception as e:
        db.rollback()
        print(f"error:{e}")
        return None
    
    
