from typing import Annotated

from fastapi import APIRouter, Path

from student_management.core.dependencies import CourseServiceDep
from student_management.schemas.course.request import (
    CourseCreateRequest,
    CourseUpdateRequest,
)
from student_management.schemas.course.response import (
    CourseResponse,
    CourseSummaryResponse,
)

router = APIRouter(prefix="/courses", tags=["Courses endpoints"])


@router.post("", response_model=CourseResponse)
async def create_course(service: CourseServiceDep, body: CourseCreateRequest):
    return await service.create_course(body)


@router.get("", response_model=list[CourseSummaryResponse])
async def get_all_courses(service: CourseServiceDep):
    return await service.list_course()


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(service: CourseServiceDep, course_id: Annotated[str, Path()]):
    return await service.get_course(course_id)


@router.get("/by-code/{course_code}", response_model=CourseResponse)
async def get_course_by_code(
    service: CourseServiceDep, course_code: Annotated[str, Path()]
):
    return await service.get_course_by_code(course_code, fetch_teacher=False)


@router.patch("/{course_id}", response_model=CourseResponse)
async def update_course(
    service: CourseServiceDep,
    course_id: Annotated[str, Path()],
    update_data: CourseUpdateRequest,
):
    return await service.update_course(course_id, update_data)


@router.delete("/{course_id}", response_model=None)
async def delete_course(service: CourseServiceDep, course_id: Annotated[str, Path()]):
    return await service.delete_course(course_id)


@router.patch("/{course_id}/unassign-teacher", response_model=CourseResponse)
async def unassign_teacher(
    service: CourseServiceDep, course_id: Annotated[str, Path()]
):
    return await service.unassign_teacher(course_id)
