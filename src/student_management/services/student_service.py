from fastapi import HTTPException, status

from student_management.core.security import hash_password, verify_password
from student_management.models.student import Student
from student_management.repositories.student_repo import StudentRepository
from student_management.schemas.student.request import (
    StudentChangePasswordRequest,
    StudentCreateRequest,
    StudentUpdateRequest,
)


class StudentService:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    async def create(self, request: StudentCreateRequest) -> Student:
        exist_email = await self.student_repo.get_by_email(request.email)
        if exist_email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Email {request.email} đã tồn tại ",
            )

        exist_student_code = await self.student_repo.get_by_student_code(
            request.student_code
        )
        if exist_student_code:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {request.email} đã tồn tại ",
            )

        password_hash = hash_password(request.password)
        return await self.student_repo.create(request, password_hash)

    async def get_student(self, student_id: str) -> Student | None:
        student = await self.student_repo.get_by_id(student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student { student_id} không tồn tại ",
            )

        return student

    async def get_student_by_email(self, email: str) -> Student | None:
        student = await self.student_repo.get_by_email(email)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student {email} không tồn tại ",
            )

        return student

    async def list_student(self) -> list[Student]:
        ds_sv = await self.student_repo.get_all()

        return ds_sv

    async def update_student(
        self, student_id: str, request: StudentUpdateRequest
    ) -> Student | None:
        updated_data = request.model_dump(exclude_unset=True, exclude_defaults=True)

        student = await self.student_repo.update(student_id, updated_data)

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student không tồn tại ",
            )

        return student

    async def delete_student(self, student_id: str) -> None:
        deleted = await self.student_repo.delete(student_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student không tồn tại ",
            )

    async def change_student_password(
        self, student_id: str, request: StudentChangePasswordRequest
    ) -> None:
        student = await self.student_repo.get_by_id(student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student không tồn tại ",
            )

        if not verify_password(request.old_password, student.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mật khẩu cũ không đúng",
            )

        password_hash = hash_password(request.new_password)

        is_updated = await self.student_repo.update_password(student_id, password_hash)

        if not is_updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student không tồn tại ",
            )
