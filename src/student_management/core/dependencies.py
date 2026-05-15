from typing import Annotated

from fastapi import Depends

from student_management.repositories.course_repo import CourseRepository
from student_management.repositories.enrollment_repo import EnrollmentRepository
from student_management.repositories.grade_repo import GradeRepository
from student_management.repositories.student_repo import StudentRepository
from student_management.repositories.teacher_repo import TeacherRepository
from student_management.services.course_service import CourseService
from student_management.services.enrollment_service import EnrollmentService
from student_management.services.grade_service import GradeService
from student_management.services.student_service import StudentService
from student_management.services.teacher_service import TeacherService


# STUDENT
def get_student_repository() -> StudentRepository:
    return StudentRepository()


StudentRepoDep = Annotated[StudentRepository, Depends(get_student_repository)]


def get_student_service(student_repo: StudentRepoDep) -> StudentService:
    return StudentService(student_repo)


StudentServiceDep = Annotated[StudentService, Depends(get_student_service)]


# TEACHER
def get_teacher_repository() -> TeacherRepository:
    return TeacherRepository()


TeacherRepoDep = Annotated[TeacherRepository, Depends(get_teacher_repository)]


def get_teacher_service(teacher_repo: TeacherRepoDep) -> TeacherService:
    return TeacherService(teacher_repo)


TeacherServiceDep = Annotated[TeacherService, Depends(get_teacher_service)]


# COURSE
def get_course_repository() -> CourseRepository:
    return CourseRepository()


CourseRepoDep = Annotated[CourseRepository, Depends(get_course_repository)]


def get_course_service(course_repo: CourseRepoDep) -> CourseService:
    return CourseService(course_repo)


CourseServiceDep = Annotated[CourseService, Depends(get_course_service)]


# ENROLLMENT
def get_enrollment_repository() -> EnrollmentRepository:
    return EnrollmentRepository()


EnrollmentRepoDep = Annotated[EnrollmentRepository, Depends(get_enrollment_repository)]


def get_enrollment_service(enrollment_repo: EnrollmentRepoDep) -> EnrollmentService:
    return EnrollmentService(enrollment_repo)


EnrollmentServiceDep = Annotated[EnrollmentService, Depends(get_enrollment_service)]


# GRADE
def get_grade_repository() -> GradeRepository:
    return GradeRepository()


GradeRepoDep = Annotated[GradeRepository, Depends(get_grade_repository)]


def get_grade_service(grade_repo: GradeRepoDep) -> GradeService:
    return GradeService(grade_repo)


GradeServiceDep = Annotated[GradeService, Depends(get_grade_service)]
