from fastapi import HTTPException, status

from student_management.repositories.grade_repo import GradeRepository
from student_management.schemas.grade.request import (
    GradeCreateRequest,
    GradeUpdateRequest,
)
from student_management.schemas.grade.response import GradeResponse


class GradeService:
    def __init__(self, grade_repo: GradeRepository):
        self.grade_repo = grade_repo

    async def create_grade(self, request: GradeCreateRequest) -> GradeResponse:
        existed_grade = await self.grade_repo.get_by_enrollment(request.enrollment_id)
        if existed_grade:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student đã đăng ký course",
            )

        try:
            grade = await self.grade_repo.create(request)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        return GradeResponse.from_document(grade)

    async def get_grade(self, grade_id: str) -> GradeResponse:
        grade = await self.grade_repo.get_by_id(grade_id)
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"grade {grade_id} không tồn tại ",
            )

        return GradeResponse.from_document(grade)

    async def get_grade_by_enrollment(self, enrollment_id: str) -> GradeResponse:
        grade = await self.grade_repo.get_by_enrollment(enrollment_id)
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="grade không tồn tại ",
            )

        return GradeResponse.from_document(grade)

    async def update_grade(
        self, grade_id: str, request: GradeUpdateRequest
    ) -> GradeResponse:
        updated_data = request.model_dump(exclude_unset=True)
        grade = await self.grade_repo.update(grade_id, updated_data)

        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="grade không tồn tại ",
            )

        return GradeResponse.from_document(grade)

    async def delete_grade(self, grade_id: str) -> None:
        grade = await self.grade_repo.delete(grade_id)
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="grade không tồn tại ",
            )

    async def assign_grader(self, grade_id: str, teacher_id: str) -> GradeResponse:
        try:
            grade = await self.grade_repo.update(grade_id, {"graded_by": teacher_id})
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="grade không tồn tại ",
            )

        return GradeResponse.from_document(grade)

    async def remove_grader(self, grade_id: str) -> GradeResponse:
        grade = await self.grade_repo.update(grade_id, {"graded_by": None})

        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="grade không tồn tại ",
            )

        return GradeResponse.from_document(grade)
