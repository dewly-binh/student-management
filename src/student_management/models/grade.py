from datetime import datetime, timezone
from typing import TYPE_CHECKING

import pymongo
from beanie import Document, Link
from pydantic import Field
from pymongo import IndexModel

if TYPE_CHECKING:
    from .enrollment import Enrollment
    from .teacher import Teacher


class Grade(Document):
    enrollment: Link["Enrollment"] = Field(...)
    midterm: float | None = Field(default=None, ge=0, le=10)
    final: float | None = Field(default=None, ge=0, le=10)
    graded_by: Link["Teacher"] | None = None
    graded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def gpa(self):
        if self.midterm is None or self.final is None:
            return None
        return round(self.midterm * 0.4 + self.final * 0.6, 2)

    class Settings:
        name = "grades"
        indexes = [IndexModel([("enrollment", pymongo.ASCENDING)], unique=True)]
