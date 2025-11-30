from fastapi import APIRouter, Depends, Query
from backend.db.models import  Attendance
from backend.db.database import get_db
from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime,date, timezone, timedelta
from backend.services.employee_service import fetch_emp_by_id
from backend.db.schemas import EmployeeIdSchema, AttendanceMonthRangeSchema, AttendanceDateRangeSchema
from backend.services.attendance_service import (
                                                get_all_employee_attendance,
                                                get_attendance_for_month,
                                                get_attendance_for_range,
                                                check_in_employee,
                                                check_out_employee)


attendanceRouter = APIRouter(
    prefix = "/attendance",
    tags = ["Attendance"]
)

@attendanceRouter.post('/checkin')
def checkInEmployee(employee_id:int, db:Session = Depends(get_db)):
    if not fetch_emp_by_id(employee_id,db):
        return {"statusCode":404, "message":" Employee no found!"}
    if db.query(Attendance).filter(Attendance.employee_details_id == employee_id, Attendance.date == date.today()).first():
        return {"statusCode":409,"message":"User already checked in."}

    if check_in_employee(employee_id,db):
        return {"statusCode":200,"message":"check in logged successfully."}
    else:
        return {"statusCode":409, "message":"check in failed."}

@attendanceRouter.put('/checkout')
def checkOutEmployee(employee_id:int, db:Session = Depends(get_db)):
    if db.query(Attendance).filter(
                                    Attendance.employee_details_id == employee_id,
                                    Attendance.date == date.today(),
                                    Attendance.check_out.isnot(None)
                                    ).first():
        return {"statusCode":409, "message":"User already checked out."}                           
    if check_out_employee(employee_id,db):
        return {"statusCode":200,"message":"check out logged successfully."}
    else:
        return {"statusCode":409, "message":"check out failed."}


@attendanceRouter.post('/employee/{employee_id}')
def get_all_attendance(employee_id: int, db: Session = Depends(get_db)):
    if db.query(Attendance).filter(Attendance.employee_details_id == employee_id,
                                   Attendance.date == date.today(),
                                   Attendance.check_out.isnot(None)).first():
        {"statusCode":409, "message":"Empoyee already checked out."}
    logs = get_all_employee_attendance(employee_id, db)
    if not logs:
        return {"statusCode":404, "message":"No Attendance Logs found"}
    return {
        "statusCode":200,
        "message":"Employee's logs fetched successfully",
        "logs": logs
    }


@attendanceRouter.get("/employee/{employee_id}")
def get_attendance_monthly(
    employee_id: int,
    month: str = Query(..., regex=r"^\d{4}-\d{2}$"),
    db: Session = Depends(get_db)
):
    schema = AttendanceMonthRangeSchema(employee_details_id=employee_id, month=month)
    logs = get_attendance_for_month(schema, db)   # <-- service function
    
    if not logs:
        return {"statusCode":404, "message":"No attendance logs found"}

    return {
        "statusCode":200,
        "message":"Attendance fetched successfully",
        "logs": logs
    }

@attendanceRouter.get("/employee/{employee_id}/range")
def get_attendance_by_range(
    employee_id: int,
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db)
):
    schema = AttendanceDateRangeSchema(
        employee_id=employee_id,
        from_date=from_date,
        to_date=to_date
    )
    logs = fetch_attendance_in_range(schema, db)
    if not logs:
        return {"statusCode": 404, "message": "No attendance logs found"}
    return {
        "statusCode": 200,
        "message": "Attendance fetched successfully",
        "logs": logs
    }
