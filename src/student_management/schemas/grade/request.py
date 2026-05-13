from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class GradeCreateRequest(BaseModel):
    enrollment_id: str
    midterm: float | None = Field(default=None, ge=0, le=10)
    final: float | None = Field(default=None, ge=0, le=10)
    graded_by: str | None = None

    @field_validator("enrollment_id", "graded_by", mode="before")
    @classmethod
    def parse_object_id(cls, v):
        if v is None:
            return None
        if ObjectId.is_valid(v):
            return str(v)
        raise ValueError("id must be a valid ObjectId")


class GradeUpdateRequest(BaseModel):
    midterm: float | None = Field(default=None, ge=0, le=10)
    final: float | None = Field(default=None, ge=0, le=10)
