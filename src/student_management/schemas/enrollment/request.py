from bson import ObjectId
from pydantic import BaseModel, Field

from student_management.models.enrollment import EnrollmentStatusEnum


class EnrollmentCreateRequest(BaseModel):
    student_id: ObjectId
    course_id: ObjectId
    semenster: str = Field(
        ...,
        pattern=r"^\d{4}-(1|2|3)$",
        examples=["2024-1"],
        description="<năm học>-<kỳ học>",
    )


class EnrollmentUpdateRequest(BaseModel):
    status: EnrollmentStatusEnum | None = None
