from student_management.models.student import Student
from student_management.schemas.student.request import StudentCreateRequest


class StudentRepository:
    async def create(self, student: StudentCreateRequest) -> Student:
        password_hash = student.password

        sv = Student(
            full_name=student.full_name,
            email=student.email,
            password_hash=password_hash,
            student_code=student.student_code,
            date_of_birth=student.date_of_birth,
            gender=student.gender,
            phone=student.phone,
            address=student.address,
        )
        await sv.insert()
        return sv # sv đại diện cho một document cụ thể / Student đại diện cho cả 1 collection
 
    async def get_by_id(self, student_id: str) -> Student | None:
        # .get() chỉ dùng được với _id
        # nếu muốn tìm theo field khác → dùng .find_one()
        return await Student.get(student_id)

    async def get_by_email(self, email: str) -> Student | None:
        return await Student.find_one(Student.email == email)

    async def get_all(self) -> list[Student]:
        return await Student.find_all().to_list()

    async def update(self, student_id: str, update_data: dict) -> Student | None:
        sv = await self.get_by_id(student_id)
        if sv is None:
            return None

        await sv.set(update_data)
        return sv

    async def delete(self, student_id: str) -> bool:
        sv = await self.get_by_id(student_id)
        if sv is None:
            return False

        await sv.delete()
        return True

    async def update_password(self, student_id: str, password_hash: str) -> bool:
        student = await self.get_by_id(student_id)
        if student is None:
            return False

        await student.set({Student.password_hash: password_hash})
        return True
