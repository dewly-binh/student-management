from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class GradeCreateRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    enrollment_id: ObjectId
    midterm: float | None = Field(default=None, ge=0, le=10)
    final: float | None = Field(default=None, ge=0, le=10)
    graded_by: ObjectId | None = None


class GradeUpdateRequest(BaseModel):
    midterm: float | None = Field(default=None, ge=0, le=10)
    final: float | None = Field(default=None, ge=0, le=10)
