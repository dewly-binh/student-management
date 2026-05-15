from typing import Annotated

from fastapi import APIRouter, Path

from student_management.core.dependencies import EnrollmentServiceDep
from student_management.schemas.enrollment.request import (
    EnrollmentCreateRequest,
    EnrollmentUpdateRequest,
)
from student_management.schemas.enrollment.response import (
    EnrollmentResponse,
    EnrollmentSummaryResponse,
)

router = APIRouter(prefix="/enrollments", tags=["Enrollment endpoints"])


@router.post("", response_model=EnrollmentResponse)
async def create_enrollment(
    service: EnrollmentServiceDep, body: EnrollmentCreateRequest
):
    return await service.create_enrollment(body)


@router.get("/lookup", response_model=EnrollmentResponse)
async def lookup_enrollment(
    service: EnrollmentServiceDep, student_id: str, course_id: str, semester: str
):
    return await service.get_enrollment_by_student_course_semester(
        student_id, course_id, semester
    )


@router.get("/{enrollment_id}", response_model=EnrollmentSummaryResponse)
async def get_enrollments_by_id(
    service: EnrollmentServiceDep, enrollment_id: Annotated[str, Path()]
):
    return await service.get_enrollment(enrollment_id)


@router.get("/by-student/{student_id}", response_model=list[EnrollmentSummaryResponse])
async def get_enrollment_by_student(
    service: EnrollmentServiceDep, student_id: Annotated[str, Path()]
):
    return await service.list_enrollments_by_student(student_id)


@router.get("/by-course/{course_id}", response_model=list[EnrollmentSummaryResponse])
async def get_enrollment_by_course(
    service: EnrollmentServiceDep, course_id: Annotated[str, Path()]
):
    return await service.list_enrollments_by_course(course_id)


@router.patch("/{enrollment_id}", response_model=EnrollmentResponse)
async def update_enrollment(
    service: EnrollmentServiceDep,
    enrollment_id: Annotated[str, Path()],
    update_data: EnrollmentUpdateRequest,
):
    return await service.update_enrollment(enrollment_id, update_data)


@router.delete("/{enrollment_id}", response_model=None)
async def delete_enrollment(
    service: EnrollmentServiceDep, enrollment_id: Annotated[str, Path()]
):
    return await service.delete_enrollment(enrollment_id)


@router.patch("/{enrollment_id}/drop", response_model=EnrollmentResponse)
async def update_status_drop(
    service: EnrollmentServiceDep, enrollment_id: Annotated[str, Path()]
):
    return await service.drop_enrollment(enrollment_id)


@router.patch("/{enrollment_id}/completed", response_model=EnrollmentResponse)
async def update_status_complete(
    service: EnrollmentServiceDep, enrollment_id: Annotated[str, Path()]
):
    return await service.complete_enrollment(enrollment_id)
