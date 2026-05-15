from fastapi import APIRouter

from student_management.core.dependencies import GradeServiceDep
from student_management.schemas.grade.request import (
    GradeCreateRequest,
    GradeUpdateRequest,
)
from student_management.schemas.grade.response import GradeResponse

router = APIRouter(prefix="/grades", tags=["Grade Enpoint"])


@router.post("", response_model=GradeResponse)
async def create_grade(service: GradeServiceDep, body: GradeCreateRequest):
    return await service.create_grade(body)


@router.get("/{grade_id}", response_model=GradeResponse)
async def get_grade_by_id(service: GradeServiceDep, grade_id: str):
    return await service.get_grade(grade_id)


@router.get("/by-enrollment/{enrollment_id}", response_model=GradeResponse)
async def get_grade_by_enrollment(service: GradeServiceDep, enrollment_id: str):
    return await service.get_grade_by_enrollment(enrollment_id)


@router.patch("/{grade_id}", response_model=GradeResponse)
async def update_grade(
    service: GradeServiceDep, grade_id: str, update_data: GradeUpdateRequest
):
    return await service.update_grade(grade_id, update_data)


@router.delete("/{grade_id}", response_model=None)
async def delete_grade(service: GradeServiceDep, grade_id: str):
    return await service.delete_grade(grade_id)


@router.patch("/{grade_id}/grader")
async def assign_grader(service: GradeServiceDep, grade_id: str, teacher_id: str):
    return await service.assign_grader(grade_id, teacher_id)


@router.delete("/{grade_id}/grader")
async def unassign_grader(service: GradeServiceDep, grade_id: str):
    return await service.remove_grader(grade_id)
