from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from student_management.models.student import GenderEnum


class StudentCreateRequest(BaseModel):
    full_name: str = Field(..., max_length=100)
    email: EmailStr = Field(
        ..., description="Email đăng nhập, không thể thay đổi sau khi tạo tài khoản"
    )
    password: str = Field(..., min_length=8)
    confirmed_password: str = Field(..., min_length=8)
    student_code: str = Field(..., pattern=r"^SV\d{3}$", examples=["SV001", "SV002"])
    date_of_birth: date | None = None
    gender: GenderEnum = GenderEnum.OTHER
    phone: str | None = Field(default=None, pattern=r"^(0|\+84)[3|5|7|8|9]\d{8}$")
    address: str | None = None

    @model_validator(mode="after")
    def check_password_match(self):
        if self.password != self.confirmed_password:
            raise ValueError("Mật khẩu không khớp")

        return self


class StudentUpdateRequest(BaseModel):
    full_name: str | None = None
    date_of_birth: date | None = None
    gender: GenderEnum | None = None
    phone: str | None = Field(default=None, pattern=r"^(0|\+84)[3|5|7|8|9]\d{8}$")
    address: str | None = None

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, v):
        if v is None:
            return v

        if isinstance(v, datetime):
            v = v.date()

        today = date.today()
        if v > today:
            raise ValueError("Ngày sinh không hợp lệ")

        age = today.year - v.year
        if (today.month, today.day) < (v.month, v.day):
            age -= 1

        if age < 18:
            raise ValueError("Phải đủ 18 tuổi")

        return v


class StudentChangePasswordRequest(BaseModel):
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
    confirmed_password: str = Field(..., min_length=8)

    @model_validator(mode="after")
    def check_password_match(self):
        if self.new_password != self.confirmed_password:
            raise ValueError("Mật khẩu không khớp")
        return self

    @model_validator(mode="after")
    def check_password_difference(self):
        if self.new_password == self.old_password:
            raise ValueError("Mật khẩu mới trùng với mật khẩu cũ")
        return self
