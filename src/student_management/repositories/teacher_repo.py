from student_management.models.teacher import Teacher
from student_management.schemas.teacher.request import TeacherCreateRequest


class TeacherRepository:
    async def create(self, teacher: TeacherCreateRequest) -> Teacher:
        password_hash = teacher.password
        tch = Teacher(
            full_name=teacher.full_name,
            email=teacher.email,
            password_hash=password_hash,
            teacher_code=teacher.teacher_code,
            department=teacher.department,
            phone=teacher.phone,
        )
        await tch.insert()
        return tch

    async def get_by_id(self, teacher_id: str) -> Teacher | None:
        return await Teacher.get(teacher_id)

    async def get_by_email(self, email: str) -> Teacher | None:
        return await Teacher.find_one(Teacher.email == email)

    async def get_by_teacher_code(self, teacher_code: str) -> Teacher | None:
        return await Teacher.find_one(Teacher.teacher_code == teacher_code)

    async def get_all(self) -> list[Teacher]:
        return await Teacher.find_all().to_list()

    async def update(self, teacher_id: str, update_data: dict) -> Teacher | None:
        tch = await self.get_by_id(teacher_id)
        if tch is None:
            return None
        await tch.set(update_data)
        return tch

    async def delete(self, teacher_id: str) -> bool:
        tch = await self.get_by_id(teacher_id)
        if tch is None:
            return False

        await tch.delete()

        return True

    async def update_password(self, teacher_id: str, password_hash: str) -> bool:
        tch = await self.get_by_id(teacher_id)
        if tch is None:
            return False
        
        await tch.set({Teacher.password_hash: password_hash})
        return True