from enum import Enum
from typing import TYPE_CHECKING

import pymongo
from beanie import Document, Link
from pydantic import Field
from pymongo import IndexModel

if TYPE_CHECKING:
    from .teacher import Teacher


class CourseStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Course(Document):
    course_code: str = Field(..., pattern=r"^[A-Z]{2,3}\d{3}$")
    name: str = Field(...)
    credits: int = Field(..., ge=1, le=5)
    description: str | None = None
    teacher: Link["Teacher"] | None = None
    status: CourseStatusEnum = Field(default=CourseStatusEnum.ACTIVE)

    class Settings:
        name = "courses"
        indexes = [IndexModel([("course_code", pymongo.ASCENDING)], unique=True)]
