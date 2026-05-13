from typing import cast

from beanie import Link

from student_management.models.course import Course
from student_management.models.teacher import Teacher
from student_management.schemas.course.request import CourseCreateRequest


_MISSING = object()


class CourseRepository:

    async def create(self, course: CourseCreateRequest) -> Course:
        teacher = None

        if course.teacher_id:
            teacher = await Teacher.get(str(course.teacher_id))
            if teacher is None:
                raise ValueError("Teacher not found")

        cous = Course(
            course_code=course.course_code,
            name=course.name,
            credits=course.credits,
            description=course.description,
            teacher=cast(Link["Teacher"] | None, teacher),
        )
        await cous.insert()
        return cous

    async def get_by_id(
        self, course_id: str, fetch_teacher: bool = False
    ) -> Course | None:
        course = await Course.get(course_id)

        # fetch_teacher ở đây là flag thông có có sử dụng edge load hay không
        if course and fetch_teacher:
            await course.fetch_link(Course.teacher)

        return course

    async def get_by_course_code(
        self, course_code: str, fetch_teacher: bool = False
    ) -> Course | None:
        course = await Course.find_one(Course.course_code == course_code)

        if course and fetch_teacher:
            await course.fetch_link(Course.teacher)

        return course

    async def get_all(self) -> list[Course]:
        course = await Course.find_all().to_list()

        return course

    async def update(self, course_id: str, update_data: dict) -> Course | None:
        course = await Course.get(course_id)

        if not course:
            return None

        update_data = update_data.copy()

        teacher_id = update_data.pop("teacher_id", _MISSING)

        if teacher_id is not _MISSING:
            if teacher_id is None:
                update_data["teacher"] = None
            else:
                teacher = await Teacher.get(str(teacher_id))

                if not teacher:
                    raise ValueError("Teacher not found")

                update_data["teacher"] = teacher

        await course.set(update_data)

        return course

    async def delete(self, course_id: str) -> bool:
        course = await self.get_by_id(course_id)

        if course is None:
            return False

        await course.delete()
        return True
