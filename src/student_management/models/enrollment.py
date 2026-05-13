from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

import pymongo
from beanie import Document, Link
from pydantic import Field
from pymongo import IndexModel

if TYPE_CHECKING:
    from .course import Course
    from .student import Student


class EnrollmentStatusEnum(str, Enum):
    ENROLLED = "enrolled"
    DROPPED = "dropped"
    COMPLETED = "completed"


class Enrollment(Document):
    student: Link["Student"] = Field(...)
    course: Link["Course"] = Field(...)
    semester: str = Field(..., pattern=r"^\d{4}-(1|2|3)$")  # 2024-1: <năm học> - <kỳ>
    enrolled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: EnrollmentStatusEnum = Field(default=EnrollmentStatusEnum.ENROLLED)

    class Settings:
        name = "enrollments"
        indexes = [
            IndexModel(
                [
                    ("student", pymongo.ASCENDING),
                    ("course", pymongo.ASCENDING),
                    ("semester", pymongo.ASCENDING),
                ],
                unique=True,
            )
        ]
