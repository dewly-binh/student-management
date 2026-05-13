from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class CourseCreateRequest(BaseModel):
    course_code: str = Field(..., pattern=r"^[A-Z]{2,3}\d{3}$")
    name: str = Field(...)
    credits: int = Field(..., ge=1, le=5)
    description: str | None = None
    teacher_id: str | None = None

    @field_validator("teacher_id", mode="before")
    @classmethod
    def parse_teacher_id(cls, v):
        if v is None:
            return None
        if ObjectId.is_valid(v):
            return str(v)
        raise ValueError("teacher_id must be a valid ObjectId")


class CourseUpdateRequest(BaseModel):
    name: str | None = None
    credits: int | None = None
    description: str | None = None
    teacher_id: str | None = None

    @field_validator("teacher_id", mode="before")
    @classmethod
    def parse_teacher_id(cls, v):
        if v is None:
            return None
        if ObjectId.is_valid(v):
            return str(v)
        raise ValueError("teacher_id must be a valid ObjectId")
