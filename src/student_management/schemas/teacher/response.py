from pydantic import BaseModel

from student_management.models.teacher import Status


class TeacherResponse(BaseModel):
    id: str
    full_name: str
    email: str
    teacher_code: str
    department: str | None
    phone: str | None
    status: Status


class TeacherSummaryResponse(BaseModel):
    id: str
    full_name: str
    teacher_code: str
    email: str
    status: Status
