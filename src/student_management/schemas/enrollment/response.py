from pydantic import BaseModel

from student_management.models.enrollment import EnrollmentStatusEnum


class EnrollmentResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    semester: str
    enrolled_at: str
    status: EnrollmentStatusEnum


class EnrollmentSummaryResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    semester: str
    status: EnrollmentStatusEnum
