from pydantic import BaseModel

from student_management.models.course import Course, CourseStatusEnum
from student_management.schemas.object_id import PyObjectId, get_link_id


class CourseResponse(BaseModel):
    id: PyObjectId
    course_code: str
    name: str
    credits: int
    description: str | None = None
    teacher_id: PyObjectId | None = None
    status: CourseStatusEnum

    @classmethod
    def from_document(cls, course: Course) -> "CourseResponse":
        return cls(
            id=course.id,
            course_code=course.course_code,
            name=course.name,
            credits=course.credits,
            description=course.description,
            teacher_id=get_link_id(course.teacher),
            status=course.status,
        )


class CourseSummaryResponse(BaseModel):
    id: PyObjectId
    course_code: str
    name: str
    credits: int
    status: CourseStatusEnum

    @classmethod
    def from_document(cls, course: Course) -> "CourseSummaryResponse":
        return cls(
            id=course.id,
            course_code=course.course_code,
            name=course.name,
            credits=course.credits,
            status=course.status,
        )
