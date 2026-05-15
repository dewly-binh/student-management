from datetime import datetime

from pydantic import BaseModel, computed_field

from student_management.models.grade import Grade
from student_management.schemas.object_id import PyObjectId, get_link_id


class GradeBase(BaseModel):
    id: PyObjectId
    enrollment_id: PyObjectId
    midterm: float | None = None
    final: float | None = None

    @computed_field
    @property
    def gpa(self) -> float | None:
        if self.midterm is None or self.final is None:
            return None
        return round(self.midterm * 0.4 + self.final * 0.6, 2)


class GradeResponse(GradeBase):
    graded_by: PyObjectId | None = None
    graded_at: datetime

    @classmethod
    def from_document(cls, grade: Grade) -> "GradeResponse":
        return cls(
            id=grade.id,
            enrollment_id=get_link_id(grade.enrollment),
            midterm=grade.midterm,
            final=grade.final,
            graded_by=get_link_id(grade.graded_by),
            graded_at=grade.graded_at,
        )


class GradeSummaryResponse(GradeBase):
    @classmethod
    def from_document(cls, grade: Grade) -> "GradeSummaryResponse":
        return cls(
            id=grade.id,
            enrollment_id=get_link_id(grade.enrollment),
            midterm=grade.midterm,
            final=grade.final,
        )
