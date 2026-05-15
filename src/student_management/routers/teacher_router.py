from typing import Annotated

from fastapi import APIRouter, Path

from student_management.core.dependencies import TeacherServiceDep
from student_management.schemas.teacher.request import (
    TeacherChangePasswordRequest,
    TeacherCreateRequest,
    TeacherUpdateRequest,
)
from student_management.schemas.teacher.response import (
    TeacherResponse,
    TeacherSummaryResponse,
)

router = APIRouter(prefix="/teachers", tags=["Teacher endpoints"])


@router.post("", response_model=TeacherResponse)
async def create_teacher(service: TeacherServiceDep, body: TeacherCreateRequest):
    return await service.create_teacher(body)


@router.get("", response_model=list[TeacherSummaryResponse])
async def get_all_teachers(service: TeacherServiceDep):
    return await service.list_teacher()


@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher(service: TeacherServiceDep, teacher_id: Annotated[str, Path()]):
    return await service.get_teacher(teacher_id)


@router.get("/by-email/{email}", response_model=TeacherResponse)
async def get_teacher_by_email(
    service: TeacherServiceDep, email: Annotated[str, Path()]
):
    return await service.get_teacher_by_email(email)


@router.patch("/{teacher_id}", response_model=TeacherResponse)
async def update_teacher_info(
    service: TeacherServiceDep,
    teacher_id: Annotated[str, Path()],
    update_data: TeacherUpdateRequest,
):
    return await service.update_teacher(teacher_id, update_data)


@router.delete("/{teacher_id}", response_model=None)
async def delete_teacher(
    service: TeacherServiceDep, teacher_id: Annotated[str, Path()]
):
    return await service.delete_teacher(teacher_id)


@router.patch("/{teacher_id}/password")
async def change_password(
    service: TeacherServiceDep,
    teacher_id: Annotated[str, Path()],
    update_data: TeacherChangePasswordRequest,
):
    return await service.change_teacher_password(teacher_id, update_data)
