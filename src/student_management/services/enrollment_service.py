from fastapi import HTTPException, status

from student_management.repositories.enrollment_repo import EnrollmentRepository
from student_management.schemas.enrollment.request import (
    EnrollmentCreateRequest,
    EnrollmentUpdateRequest,
)
from student_management.schemas.enrollment.response import (
    EnrollmentResponse,
    EnrollmentSummaryResponse,
)


class EnrollmentService:
    def __init__(self, enrollment_repo: EnrollmentRepository):
        self.enrollment_repo = enrollment_repo

    async def create_enrollment(
        self, request: EnrollmentCreateRequest
    ) -> EnrollmentResponse:
        enrollment = await self.enrollment_repo.get_by_student_course_semester(
            student_id=request.student_id,
            course_id=request.course_id,
            semester=request.semester,
        )

        if enrollment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student đã đăng ký course",
            )

        try:
            enrollment = await self.enrollment_repo.create(request)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        return EnrollmentResponse.from_document(enrollment)

    async def get_enrollment(self, enrollment_id: str) -> EnrollmentResponse:
        enrollment = await self.enrollment_repo.get_by_id(enrollment_id)
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"enrollment { enrollment_id} không tồn tại ",
            )

        return EnrollmentResponse.from_document(enrollment)

    async def list_enrollments_by_student(
        self, student_id: str
    ) -> list[EnrollmentSummaryResponse]:
        enrollments = await self.enrollment_repo.get_by_student(student_id)

        return [
            EnrollmentSummaryResponse.from_document(enrollment)
            for enrollment in enrollments
        ]

    async def list_enrollments_by_course(
        self, course_id: str
    ) -> list[EnrollmentSummaryResponse]:
        enrollments = await self.enrollment_repo.get_by_course(course_id)

        return [
            EnrollmentSummaryResponse.from_document(enrollment)
            for enrollment in enrollments
        ]

    async def get_enrollment_by_student_course_semester(
        self,
        student_id: str,
        course_id: str,
        semester: str,
    ) -> EnrollmentResponse:
        enrollment = await self.enrollment_repo.get_by_student_course_semester(
            student_id=student_id, course_id=course_id, semester=semester
        )
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="enrollment không tồn tại ",
            )
        return EnrollmentResponse.from_document(enrollment)

    async def update_enrollment(
        self, enrollment_id: str, request: EnrollmentUpdateRequest
    ) -> EnrollmentResponse:
        updated_data = request.model_dump(exclude_unset=True)
        enrollment = await self.enrollment_repo.update(enrollment_id, updated_data)

        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="enrollment không tồn tại ",
            )

        return EnrollmentResponse.from_document(enrollment)

    async def delete_enrollment(self, enrollment_id: str) -> None:
        enrollment = await self.enrollment_repo.delete(enrollment_id)
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="enrollment không tồn tại ",
            )

    async def drop_enrollment(self, enrollment_id: str) -> EnrollmentResponse:
        enrollment = await self.enrollment_repo.update(
            enrollment_id, {"status": "dropped"}
        )
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="enrollment không tồn tại ",
            )

        return EnrollmentResponse.from_document(enrollment)

    async def complete_enrollment(self, enrollment_id: str) -> EnrollmentResponse:
        enrollment = await self.enrollment_repo.update(
            enrollment_id, {"status": "completed"}
        )
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="enrollment không tồn tại ",
            )

        return EnrollmentResponse.from_document(enrollment)
