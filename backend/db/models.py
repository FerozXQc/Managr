# models.py
import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Date, Float,
    ForeignKey, Enum, func, UniqueConstraint
)
from sqlalchemy.orm import relationship
from .database import Base


class UserRole(enum.Enum):
    EMPLOYEE = "employee"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class EmployeeStatus(enum.Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    INACTIVE = "inactive"

class AttendanceStatus(enum.Enum):
    PRESENT = "Present"
    ABSENT = "Absent"
    LEAVE = "Leave"

class Employee(Base):
    __tablename__ = "employees"
    id            = Column(Integer, primary_key=True, index=True)
    full_name     = Column(String(100), nullable=False)
    email         = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    auth_role     = Column(Enum(UserRole), default=UserRole.EMPLOYEE)  # ← NEW
    is_active     = Column(Boolean, default=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

    details = relationship(
        "EmployeeDetails",
        back_populates="employee",
        uselist=False,
        cascade="all, delete-orphan"
    )


class EmployeeDetails(Base):
    __tablename__ = "employee_details"
    id              = Column(Integer, primary_key=True)
    employee_id     = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    phone           = Column(String(20), unique=True, nullable=True)
    department_id   = Column(Integer, ForeignKey("departments.id"), nullable=False)
    job_title_id    = Column(Integer, ForeignKey("roles.id"), nullable=False)
    join_date       = Column(DateTime(timezone=True), server_default=func.now())
    status          = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)

    employee        = relationship("Employee", back_populates="details")
    department      = relationship("Department")
    job_title       = relationship("Role")   # renamed for clarity
    attendance_logs = relationship("Attendance", back_populates="employee_details")


class Department(Base):
    __tablename__ = "departments"
    id          = Column(Integer, primary_key=True)
    name        = Column(String(50), unique=True, nullable=False)
    description = Column(String(200), nullable=True)

class Role(Base):                                 # ← this is JOB TITLE, not auth role
    __tablename__ = "roles"
    id          = Column(Integer, primary_key=True)
    name        = Column(String(50), unique=True, nullable=False)   # e.g. "Backend Engineer"
    description = Column(String(200), nullable=True)

class Attendance(Base):
    __tablename__ = "attendance"
    id                   = Column(Integer, primary_key=True)
    employee_details_id  = Column(Integer, ForeignKey("employee_details.id"), nullable=False)
    date                 = Column(Date, nullable=False, default=func.current_date())
    status               = Column(Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)
    check_in             = Column(DateTime(timezone=True), default=func.now())
    check_out            = Column(DateTime(timezone=True), nullable=True)
    total_hours          = Column(Float, nullable=True)
    employee_details     = relationship("EmployeeDetails", back_populates="attendance_logs")
    __table_args__ = (UniqueConstraint("employee_details_id", "date", name="uq_employee_date"),)