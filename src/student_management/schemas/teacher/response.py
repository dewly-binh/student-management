from pydantic import BaseModel

from student_management.models.teacher import Status
from student_management.schemas.object_id import PyObjectId


class TeacherResponse(BaseModel):
    id: PyObjectId
    full_name: str
    email: str
    teacher_code: str
    department: str | None
    phone: str | None
    status: Status


class TeacherSummaryResponse(BaseModel):
    id: PyObjectId
    full_name: str
    teacher_code: str
    email: str
    status: Status
