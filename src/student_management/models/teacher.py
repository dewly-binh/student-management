from enum import Enum

import pymongo
from beanie import Document
from pydantic import Field
from pymongo import IndexModel


class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Teacher(Document):
    full_name: str = Field(...)
    email: str = Field(...)
    password_hash: str = Field(...)
    teacher_code: str = Field(..., pattern=r"^GV\d{3}$")
    department: str | None = None
    phone: str | None = None
    status: Status = Field(default=Status.ACTIVE)

    class Settings:
        name = "teachers"
        indexes = [
            IndexModel([("email", pymongo.ASCENDING)], unique=True),
            IndexModel([("teacher_code", pymongo.ASCENDING)], unique=True),
        ]
