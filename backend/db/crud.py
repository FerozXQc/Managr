from .models import (Employee,Department,Role,Attendance)
from .schemas import EmployeeCreate
from sqlalchemy.orm import Session

def fetch_emp_by_id(empid:int,db:Session):
    user = db.query(Employee).filter(Employee.id == empid).first()
    print(user)
    return user

def create_employee(EmployeeCreate,db:Session):
    emp = Employee(**EmployeeCreate.dict())
    try:
        db.add(emp)
        db.commit()
        print(emp)
    except Exception as e:
        print(f"error: {e}")
        db.rollback()
    finally:
        db.close()

def delete_employee(empid:int,db:Session):
    user = fetch_emp_by_id(empid,db)
    if not user:
        return False
    try:
        db.delete(user)
        db.commit()

    except Exception as e:
        print("error: {e}")
        db.rollback()
    finally:
        db.close()

