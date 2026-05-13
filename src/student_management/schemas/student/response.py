from datetime import date, datetime

from pydantic import BaseModel

from student_management.models.student import GenderEnum, StudentStatusEnum


class StudentResponse(BaseModel):
    id: str
    full_name: str
    email: str
    student_code: str
    date_of_birth: date | None
    gender: GenderEnum
    phone: str | None
    address: str | None
    status: StudentStatusEnum
    created_at: datetime

class StudentSummaryResponse(BaseModel): 
    id: str 
    full_name: str 
    student_code: str 
    email: str 
    status: StudentStatusEnum