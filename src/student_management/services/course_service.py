from fastapi import HTTPException, status

from student_management.repositories.course_repo import CourseRepository
from student_management.schemas.course.request import (
    CourseCreateRequest,
    CourseUpdateRequest,
)
from student_management.schemas.course.response import (
    CourseResponse,
    CourseSummaryResponse,
)


class CourseService:
    def __init__(self, course_repo: CourseRepository) -> None:
        self.course_repo = course_repo

    async def create_course(self, request: CourseCreateRequest) -> CourseResponse:
        exist_course_code = await self.course_repo.get_by_course_code(
            request.course_code
        )
        if exist_course_code:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {request.course_code} đã tồn tại ",
            )

        try:
            course = await self.course_repo.create(request)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        return CourseResponse.from_document(course)

    async def get_course(self, course_id: str) -> CourseResponse:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"course { course_id} không tồn tại ",
            )

        return CourseResponse.from_document(course)

    async def get_course_by_code(
        self, course_code: str, fetch_teacher: bool = False
    ) -> CourseResponse:
        course = await self.course_repo.get_by_course_code(course_code, fetch_teacher)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"course {course} không tồn tại ",
            )

        return CourseResponse.from_document(course)

    async def list_course(self) -> list[CourseSummaryResponse]:
        ds_sv = await self.course_repo.get_all()

        return [CourseSummaryResponse.from_document(course) for course in ds_sv]

    async def update_course(
        self, course_id: str, request: CourseUpdateRequest
    ) -> CourseResponse:
        updated_data = request.model_dump(exclude_unset=True)

        try:
            course = await self.course_repo.update(course_id, updated_data)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="course không tồn tại ",
            )

        return CourseResponse.from_document(course)

    async def delete_course(self, course_id: str) -> None:
        deleted = await self.course_repo.delete(course_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="course không tồn tại ",
            )

    async def unassign_teacher(self, course_id: str) -> CourseResponse:
        updated_course = await self.course_repo.update(course_id, {"teacher_id": None})
        if updated_course is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course không tồn tại",
            )

        return CourseResponse.from_document(updated_course)
