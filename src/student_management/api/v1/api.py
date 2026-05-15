from fastapi import APIRouter

from student_management.routers.course_router import router as course_router
from student_management.routers.enrollment_router import router as enrollment_router
from student_management.routers.grade_router import router as grade_router
from student_management.routers.student_router import router as student_router
from student_management.routers.teacher_router import router as teacher_router

router = APIRouter(prefix="/v1")

router.include_router(student_router)
router.include_router(teacher_router)
router.include_router(course_router)
router.include_router(enrollment_router)
router.include_router(grade_router)
