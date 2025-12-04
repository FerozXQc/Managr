from backend.db.models import Attendance
from backend.db.schemas import EmployeeIdSchema, AttendanceDateRangeSchema, AttendanceMonthRangeSchema
from sqlalchemy.orm import Session
from datetime import datetime,date, timezone, timedelta
import calendar

def check_in_employee(employee_id:int,db:Session):
    log = Attendance(employee_details_id=employee_id)
    try:
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except Exception as e:
        db.rollback()
        print(f"Error creating attendance log: {e}")
        return None


def check_out_employee(employee_id:int, db:Session):
    log = db.query(Attendance).filter(Attendance.employee_details_id == employee_id, Attendance.date == date.today()).first()
    if not log:
        return None
    try:
        log.check_out = datetime.now(timezone.utc)
        if log.check_in.tzinfo is None:
            log.check_in = log.check_in.replace(tzinfo=timezone.utc)
        delta = log.check_out - log.check_in
        log.total_hours = (round(delta.total_seconds() / 3600, 2)) if log.check_out else None
        db.commit()
        db.refresh(log)
        return log
    except Exception as e:
        db.rollback()
        print(f"Error updating attendance log: {e}")
        return None

def get_all_employee_attendance(employee_id:EmployeeIdSchema,db:Session):
    return db.query(Attendance).filter(Attendance.id == employee_id).all()

def get_attendance_for_range(schema:AttendanceDateRangeSchema,db:Session):
    return db.query(Attendance).filter(
        Attendance.employee_id == schema.employee_id,
        Attendance.date >= schema.from_date,
        Attendance.date <= schema.to_date
        ).all()

def get_attendance_for_month(schema:AttendanceMonthRangeSchema,db:Session):
    year, month_num = map(int, schema.month.split("-"))
    start_date = date(year, month_num, 1)
    last_day = calendar.monthrange(year, month_num)[1]
    end_date = date(year, month_num, last_day)

    return (
        db.query(Attendance)
        .filter(Attendance.employee_details_id == schema.employee_details_id)
        .filter(Attendance.date.between(start_date, end_date))
        .all()
    )

