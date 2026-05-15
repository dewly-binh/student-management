from datetime import datetime

from pydantic import BaseModel

from student_management.models.enrollment import Enrollment, EnrollmentStatusEnum
from student_management.schemas.object_id import PyObjectId, get_link_id


class EnrollmentResponse(BaseModel):
    id: PyObjectId
    student_id: PyObjectId
    course_id: PyObjectId
    semester: str
    enrolled_at: datetime
    status: EnrollmentStatusEnum

    @classmethod
    def from_document(cls, enrollment: Enrollment) -> "EnrollmentResponse":
        return cls(
            id=enrollment.id,
            student_id=get_link_id(enrollment.student),
            course_id=get_link_id(enrollment.course),
            semester=enrollment.semester,
            enrolled_at=enrollment.enrolled_at,
            status=enrollment.status,
        )


class EnrollmentSummaryResponse(BaseModel):
    id: PyObjectId
    student_id: PyObjectId
    course_id: PyObjectId
    semester: str
    status: EnrollmentStatusEnum

    @classmethod
    def from_document(cls, enrollment: Enrollment) -> "EnrollmentSummaryResponse":
        return cls(
            id=enrollment.id,
            student_id=get_link_id(enrollment.student),
            course_id=get_link_id(enrollment.course),
            semester=enrollment.semester,
            status=enrollment.status,
        )
