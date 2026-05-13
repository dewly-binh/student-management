from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from student_management.models.enrollment import EnrollmentStatusEnum


class EnrollmentCreateRequest(BaseModel):
    student_id: str
    course_id: str
    semester: str = Field(
        ...,
        pattern=r"^\d{4}-(1|2|3)$",
        examples=["2024-1"],
        description="<năm học>-<kỳ học>",
    )

    @field_validator("student_id", "course_id", mode="before")
    @classmethod
    def parse_object_id(cls, v):
        if ObjectId.is_valid(v):
            return str(v)
        raise ValueError("id must be a valid ObjectId")


class EnrollmentUpdateRequest(BaseModel):
    status: EnrollmentStatusEnum | None = None
