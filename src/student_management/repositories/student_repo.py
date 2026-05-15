from student_management.db.mongo_types import encode_mongo_update, parse_object_id
from student_management.models.student import Student
from student_management.schemas.student.request import StudentCreateRequest


class StudentRepository:
    async def create(
        self, student: StudentCreateRequest, password_hash: str
    ) -> Student:
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
        return sv  # sv đại diện cho một document cụ thể / Student đại diện cho cả 1 collection

    async def get_by_id(self, student_id: str) -> Student | None:
        # .get() chỉ dùng được với _id
        # nếu muốn tìm theo field khác → dùng .find_one()
        return await Student.get(student_id)

    async def get_by_email(self, email: str) -> Student | None:
        return await Student.find_one(Student.email == email)

    async def get_by_student_code(self, student_code: str) -> Student | None:
        return await Student.find_one(Student.student_code == student_code)

    async def get_all(self) -> list[Student]:
        return await Student.find_all().to_list()

    async def update(self, student_id: str, update_data: dict) -> Student | None:
        object_id = parse_object_id(student_id)
        if object_id is None:
            return None

        # Bypass Beanie.get() here so an invalid old document can still be fixed.
        # Request validation must happen before this direct Mongo update.
        result = await Student.get_pymongo_collection().update_one(
            {"_id": object_id},
            {"$set": encode_mongo_update(update_data)},
        )

        if result.matched_count == 0:
            return None

        return await self.get_by_id(student_id)

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
