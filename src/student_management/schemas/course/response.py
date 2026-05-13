from pydantic import BaseModel

from student_management.models.course import CourseStatusEnum


class CourseResponse(BaseModel):
    id: str
    course_code: str
    name: str
    credits: int
    description: str | None = None
    teacher_id: str | None = None
    status: CourseStatusEnum


class CourseSummaryResponse(BaseModel):
    id: str
    course_code: str
    name: str
    credits: int
    status: CourseStatusEnum
