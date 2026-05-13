from datetime import datetime

from pydantic import BaseModel, computed_field


class GradeBase(BaseModel):
    id: str
    enrollment_id: str
    midterm: float | None = None
    final: float | None = None

    @computed_field
    @property
    def gpa(self) -> float | None:
        if self.midterm is None or self.final is None:
            return None
        return round(self.midterm * 0.4 + self.final * 0.6, 2)


class GradeResponse(GradeBase):
    graded_by: str | None = None
    graded_at: datetime


class GradeSummaryResponse(GradeBase):
    pass
