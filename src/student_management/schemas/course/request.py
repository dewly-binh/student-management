from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator


class CourseCreateRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    course_code: str = Field(..., pattern=r"^[A-Z]{2,3}\d{3}$")
    name: str = Field(...)
    credits: int = Field(..., ge=1, le=5)
    description: str | None = None
    teacher_id: ObjectId | None = None

    @field_validator("teacher_id", mode="before")
    @classmethod
    def parse_teacher_id(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return ObjectId(v)  # parse str → ObjectId
        return v


class CourseUpdateRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str | None = None
    credits: int | None = None
    description: str | None = None
    teacher_id: ObjectId | None = None

    @field_validator("teacher_id", mode="before")
    @classmethod
    def parse_teacher_id(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return ObjectId(v)  # parse str → ObjectId
        return v
