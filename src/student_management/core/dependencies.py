from typing import Annotated

from fastapi import Depends

from student_management.repositories.course_repo import CourseRepository
from student_management.repositories.enrollment_repo import EnrollmentRepository
from student_management.repositories.grade_repo import GradeRepository
from student_management.repositories.student_repo import StudentRepository
from student_management.repositories.teacher_repo import TeacherRepository


# STUDENT
def get_student_repository() -> StudentRepository:
    return StudentRepository()


StudentRepoDep = Annotated[StudentRepository, Depends(get_student_repository)]


# TEACHER
def get_teacher_repository() -> TeacherRepository:
    return TeacherRepository()


TeacherRepoDep = Annotated[TeacherRepository, Depends(get_teacher_repository)]


# COURSE
def get_course_repository() -> CourseRepository:
    return CourseRepository()


CourseRepoDep = Annotated[CourseRepository, Depends(get_course_repository)]


# ENROLLMENT
def get_enrollment_repository() -> EnrollmentRepository:
    return EnrollmentRepository()


EnrollmentRepoDep = Annotated[EnrollmentRepository, Depends(get_enrollment_repository)]


# GRADE
def get_grade_repository() -> GradeRepository:
    return GradeRepository()


GradeRepoDep = Annotated[GradeRepository, Depends(get_grade_repository)]
