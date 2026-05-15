from typing import cast

from beanie import Link, PydanticObjectId

from student_management.models.course import Course
from student_management.models.enrollment import Enrollment
from student_management.models.student import Student
from student_management.schemas.enrollment.request import EnrollmentCreateRequest

Enrollment.model_rebuild()


class EnrollmentRepository:
    async def create(self, request: EnrollmentCreateRequest) -> Enrollment:
        student, course = None, None
        if request.course_id:
            # Link fields need the referenced document, not only its raw id.
            course = await Course.get(str(request.course_id))
        if request.student_id:
            student = await Student.get(str(request.student_id))

        if course is None:
            raise ValueError("Course not found")
        if student is None:
            raise ValueError("Student not found")

        enrollment = Enrollment(
            student=cast(Link["Student"], student),
            course=cast(Link["Course"], course),
            semester=request.semester,
        )
        await enrollment.insert()
        return enrollment

    async def get_by_id(self, enrollment_id: str) -> Enrollment | None:
        return await Enrollment.get(enrollment_id)

    async def get_by_student(self, student_id: str) -> list[Enrollment]:
        return await Enrollment.find_many(
            Enrollment.student.id == PydanticObjectId(student_id)
        ).to_list()

    async def get_by_course(self, course_id: str) -> list[Enrollment]:
        """
        Khi bạn dùng Link[Student] trong Beanie, MongoDB không lưu trực tiếp object mà lưu dưới dạng DBRef:
        // Trong MongoDB thực tế trông như thế này
        {
            "_id": ObjectId("6a0581d8..."),
            "student": {
                "$ref": "students",       // ← tên collection
                "$id": ObjectId("6a054a32...")  // ← chỉ lưu ID thôi
            },
            "course": {
                "$ref": "courses",
                "$id": ObjectId("6a057844...")
            }
        }
        """
        return await Enrollment.find_many(
            Enrollment.course.id == PydanticObjectId(course_id)
        ).to_list()

    async def get_by_student_course_semester(
        self, student_id: str, course_id: str, semester: str
    ) -> Enrollment | None:
        student = await Student.get(str(student_id))
        course = await Course.get(str(course_id))
        print(f"student: {student}")
        print(f"course: {course}")

        if student is None or course is None:
            return None

        return await Enrollment.find_one(
            Enrollment.student.id == PydanticObjectId(student.id),
            Enrollment.course.id == PydanticObjectId(course.id),
            Enrollment.semester == semester,
        )

    async def update(self, enrollment_id: str, update_data: dict) -> Enrollment | None:
        enrollment = await self.get_by_id(enrollment_id)
        if enrollment is None:
            return None

        await enrollment.set(update_data)
        return enrollment

    async def delete(self, enrollment_id: str) -> bool:
        enrollment = await self.get_by_id(enrollment_id)
        if enrollment is None:
            return False

        await enrollment.delete()
        return True
