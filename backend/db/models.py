from sqlalchemy import DateTime,UniqueConstraint,Integer, Column,Enum,Date,Time,Float,String, func, ForeignKey
from sqlalchemy.orm import declarative_base,relationship
from datetime import datetime
from .database import Base
import enum

class AttendanceStatus(enum.Enum):
    PRESENT = "Present"
    ABSENT = "Absent"
    LEAVE = "Leave"

class EmployeeStatus(enum.Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    INACTIVE = "inactive"

class Employee(Base):
    __tablename__ = 'employees'
    employee_id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    phone = Column(String(100),unique=True,nullable=False)
    department_id = Column(Integer,ForeignKey("departments.id"),nullable=False)
    role_id = Column(Integer,ForeignKey("roles.id"),nullable=False)
    department = relationship("Department", back_populates="employees")
    role = relationship("Role", back_populates="employees")
    attendance_logs = relationship("Attendance", back_populates="employee")
    join_date = Column(DateTime, server_default=func.now())
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)

    def __repr__(self):
        return f"<Employee(id='{self.employee_id}',name='{self.name}',department_id='{self.department_id}', role_id='{self.role_id}',join_date='{self.join_date}',status='{self.status}')>"

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer,primary_key=True,index=True)
    department = Column(String(50),unique=True,nullable=False)
    description = Column(String(100))
    employees = relationship("Employee",back_populates="department")

    def __repr__(self):
        return f"<Department(id='{self.id}',dept='{self.department}',description='{self.description}')>"

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer,primary_key=True,index=True)
    role = Column(String(50),unique=True,nullable=False)
    description = Column(String(100))
    employees = relationship("Employee",back_populates="role")

    def __repr__(self):
        return f"<Role(id='{self.id}',role='{self.role}',description='{self.description}')>"

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    date = Column(Date, nullable=False, server_default=func.current_date())
    status = Column(Enum(AttendanceStatus), nullable=False, default=AttendanceStatus.PRESENT)
    check_in = Column(DateTime(timezone=True), server_default=func.now())
    check_out = Column(DateTime(timezone=True), nullable=True)
    total_hours = Column(Float, nullable=True)
    employee = relationship("Employee", back_populates="attendance_logs")

    __table_args__ = (
        UniqueConstraint("employee_id", "date", name="unique_attendance_per_day"),
    )