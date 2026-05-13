from datetime import date, datetime, timezone
from enum import Enum

import pymongo
from beanie import Document
from pydantic import EmailStr, Field, field_validator
from pymongo import IndexModel


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class StudentStatusEnum(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    GRADUATED = "graduated"


class Student(Document):
    full_name: str = Field(max_length=100)
    email: EmailStr = Field(...)
    password_hash: str = Field(...)
    student_code: str = Field(..., pattern=r"^SV\d{3}$")
    date_of_birth: date | None = None
    gender: GenderEnum = Field(default=GenderEnum.OTHER)
    phone: str | None = Field(default=None, pattern=r"^(0|\+84)[3|5|7|8|9]\d{8}$")
    address: str | None = None
    status: StudentStatusEnum = Field(default=StudentStatusEnum.ACTIVE)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, v):
        if v is None:
            return v

        today = date.today()
        if v > today:
            raise ValueError("Ngày sinh không hợp lệ")
        age = today.year - v.year

        if (today.month, today.day) < (v.month, v.day):
            age -= 1

        if age < 18:
            raise ValueError("Phải đủ 18 tuổi")

        return v

    class Settings:
        name = "students"
        indexes = [
            IndexModel([("email", pymongo.ASCENDING)], unique=True),
            IndexModel([("student_code", pymongo.ASCENDING)], unique=True),
        ]
