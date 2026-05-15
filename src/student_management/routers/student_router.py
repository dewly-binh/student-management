from typing import Annotated

from fastapi import APIRouter, Body, Path

from student_management.core.dependencies import StudentServiceDep
from student_management.schemas.student.request import (
    StudentChangePasswordRequest,
    StudentCreateRequest,
    StudentUpdateRequest,
)
from student_management.schemas.student.response import (
    StudentResponse,
    StudentSummaryResponse,
)

router = APIRouter(prefix="/students", tags=["Student endpoints"])


@router.post("", response_model=StudentResponse)
async def create_student(service: StudentServiceDep, body: StudentCreateRequest):
    return await service.create(request=body)


@router.get("", response_model=list[StudentSummaryResponse])
async def get_all_students(service: StudentServiceDep):
    return await service.list_student()


@router.get("/{student_id}", response_model=StudentSummaryResponse)
async def get_student(service: StudentServiceDep, student_id: Annotated[str, Path()]):
    return await service.get_student(student_id)


@router.get("/by-email/{email}", response_model=StudentSummaryResponse)
async def get_student_by_email(
    service: StudentServiceDep, email: Annotated[str, Path()]
):
    return await service.get_student_by_email(email)


@router.patch("/{student_id}", response_model=StudentResponse)
async def update_student_info(
    service: StudentServiceDep,
    student_id: Annotated[str, Path()],
    updated_data: Annotated[StudentUpdateRequest, Body()],
):
    return await service.update_student(student_id, updated_data)


@router.delete("/{student_id}", response_model=None)
async def delete_student(
    service: StudentServiceDep, student_id: Annotated[str, Path()]
):
    return await service.delete_student(student_id)


@router.patch("/{student_id}/password", response_model=None)
async def update_password(
    service: StudentServiceDep,
    student_id: Annotated[str, Path()],
    change_password: StudentChangePasswordRequest,
):
    return await service.change_student_password(student_id, change_password)
