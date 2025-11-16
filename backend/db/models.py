from sqlalchemy import (
    DateTime, UniqueConstraint, Integer, Column, Enum, Date,
    Float, String, ForeignKey, func
)
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import datetime


# -------------------------
# ENUMS
# -------------------------

class AttendanceStatus(enum.Enum):
    PRESENT = "Present"
    ABSENT = "Absent"
    LEAVE = "Leave"


class EmployeeStatus(enum.Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    INACTIVE = "inactive"


# -------------------------
# EMPLOYEE BASE TABLE
# -------------------------

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # One-to-one relationship
    details = relationship("EmployeeDetails", back_populates="employee", uselist=False)

    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.full_name}', email='{self.email}')>"


# -------------------------
# EMPLOYEE DETAILS (1-1)
# -------------------------

class EmployeeDetails(Base):
    __tablename__ = 'employee_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)

    phone = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    join_date = Column(DateTime, server_default=func.now())
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)

    # Relationships
    employee = relationship("Employee", back_populates="details")
    department = relationship("Department", back_populates="employee_details")
    role = relationship("Role", back_populates="employee_details")
    attendance_logs = relationship("Attendance", back_populates="employee_details")

    def __repr__(self):
        return (
            f"<EmployeeDetails(id={self.id}, employee_id={self.employee_id}, "
            f"department_id={self.department_id}, role_id={self.role_id}, "
            f"status={self.status.value})>"
        )


# -------------------------
# DEPARTMENT TABLE
# -------------------------

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String(50), unique=True, nullable=False)
    description = Column(String(100))

    employee_details = relationship("EmployeeDetails", back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.id}, dept='{self.department}')>"


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50), unique=True, nullable=False)
    description = Column(String(100))
    employee_details = relationship("EmployeeDetails", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, role='{self.role}')>"

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_details_id = Column(Integer, ForeignKey("employee_details.id"), nullable=False)
    date = Column(Date, nullable=False, server_default=func.current_date())
    status = Column(Enum(AttendanceStatus), nullable=False, default=AttendanceStatus.PRESENT)
    check_in = Column(DateTime(timezone=True), server_default=func.now())
    check_out = Column(DateTime(timezone=True), nullable=True)
    total_hours = Column(Float, nullable=True)

    employee_details = relationship("EmployeeDetails", back_populates="attendance_logs")

    __table_args__ = (
        UniqueConstraint("employee_details_id", "date", name="unique_attendance_per_day"),
    )

    def __repr__(self):
        return f"<Attendance(id={self.id}, employee_details_id={self.employee_details_id}, date={self.date})>"
