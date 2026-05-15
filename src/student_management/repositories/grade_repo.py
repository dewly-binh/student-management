from typing import cast

from beanie import Link, PydanticObjectId

from student_management.models.enrollment import Enrollment
from student_management.models.grade import Grade
from student_management.models.teacher import Teacher
from student_management.schemas.grade.request import GradeCreateRequest

_MISSING = object()

Grade.model_rebuild()


class GradeRepository:
    async def create(self, request: GradeCreateRequest) -> Grade:
        enrollment = None
        if request.enrollment_id:
            # Link fields need the referenced document, not only its raw id.
            enrollment = await Enrollment.get(str(request.enrollment_id))
            if enrollment is None:
                raise ValueError("Enrollment not found")

        teacher = None
        if request.graded_by:
            teacher = await Teacher.get(str(request.graded_by))
            if teacher is None:
                raise ValueError("Teacher not found")

        grade = Grade(
            enrollment=cast(Link["Enrollment"], enrollment),
            midterm=request.midterm,
            final=request.final,
            graded_by=cast(Link["Teacher"] | None, teacher),
        )

        await grade.insert()
        return grade

    async def get_by_id(self, grade_id: str) -> Grade | None:
        return await Grade.get(grade_id)

    async def get_by_enrollment(self, enrollment_id: str) -> Grade | None:
        enrollment = await Enrollment.get(str(enrollment_id))
        if enrollment is None:
            return None

        # Query Link fields with the linked document so Beanie builds the correct DBRef.
        return await Grade.find_one(
            Grade.enrollment.id == PydanticObjectId(enrollment.id)
        )

    async def update(self, grade_id: str, update_data: dict) -> Grade | None:
        grade = await self.get_by_id(grade_id)
        if grade is None:
            return None

        update_data = update_data.copy()

        graded_by = update_data.pop("graded_by", _MISSING)

        if graded_by is not _MISSING:
            if graded_by is None:
                update_data["graded_by"] = None
            else:
                teacher = await Teacher.get(str(graded_by))
                if teacher is None:
                    raise ValueError("Teacher not found")

                update_data["graded_by"] = teacher

        await grade.set(update_data)
        return grade

    async def delete(self, grade_id: str) -> bool:
        grade = await self.get_by_id(grade_id)
        if grade is None:
            return False

        await grade.delete()

        return True
