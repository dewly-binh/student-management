from fastapi import HTTPException, status

from student_management.core.security import hash_password, verify_password
from student_management.models.teacher import Teacher
from student_management.repositories.teacher_repo import TeacherRepository
from student_management.schemas.teacher.request import (
    TeacherChangePasswordRequest,
    TeacherCreateRequest,
    TeacherUpdateRequest,
)


class TeacherService:
    def __init__(self, teacher_repo: TeacherRepository):
        self.teacher_repo = teacher_repo

    async def create_teacher(self, request: TeacherCreateRequest) -> Teacher:
        password_hash = hash_password(request.password)

        exist_email = await self.teacher_repo.get_by_email(request.email)
        if exist_email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Email {request.email} đã tồn tại ",
            )

        exist_teacher_code = await self.teacher_repo.get_by_teacher_code(
            request.teacher_code
        )
        if exist_teacher_code:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {request.teacher_code} đã tồn tại ",
            )

        teacher = await self.teacher_repo.create(request, password_hash)

        return teacher

    async def get_teacher(self, teacher_id: str) -> Teacher | None:
        teacher = await self.teacher_repo.get_by_id(teacher_id)
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"teacher { teacher_id} không tồn tại ",
            )

        return teacher

    async def get_teacher_by_email(self, email: str) -> Teacher | None:
        teacher = await self.teacher_repo.get_by_email(email)
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"teacher {email} không tồn tại ",
            )

        return teacher

    async def list_teacher(self) -> list[Teacher]:
        ds_sv = await self.teacher_repo.get_all()

        return ds_sv

    async def update_teacher(
        self, teacher_id: str, request: TeacherUpdateRequest
    ) -> Teacher | None:
        updated_data = request.model_dump(exclude_unset=True, exclude_defaults=True)

        teacher = await self.teacher_repo.update(teacher_id, updated_data)

        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="teacher không tồn tại ",
            )

        return teacher

    async def delete_teacher(self, teacher_id: str) -> None:
        deleted = await self.teacher_repo.delete(teacher_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="teacher không tồn tại ",
            )

    async def change_teacher_password(
        self, teacher_id: str, request: TeacherChangePasswordRequest
    ) -> None:
        teacher = await self.teacher_repo.get_by_id(teacher_id)
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="teacher không tồn tại ",
            )

        if not verify_password(request.old_password, teacher.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mật khẩu cũ không đúng",
            )

        password_hash = hash_password(request.new_password)

        is_updated = await self.teacher_repo.update_password(teacher_id, password_hash)

        if not is_updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="teacher không tồn tại ",
            )
