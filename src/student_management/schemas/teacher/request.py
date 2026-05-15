from pydantic import BaseModel, EmailStr, Field, model_validator


class TeacherCreateRequest(BaseModel):
    full_name: str = Field(...)
    email: EmailStr = Field(
        ..., description="Email đăng nhập, không thể thay đổi sau khi tạo tài khoản"
    )
    password: str = Field(..., min_length=8)
    confirmed_password: str = Field(..., min_length=8)
    teacher_code: str = Field(..., pattern=r"^GV\d{3}$")
    department: str | None = None
    phone: str | None = Field(default=None, pattern=r"^(0|\+84)[3|5|7|8|9]\d{8}$")

    @model_validator(mode="after")
    def check_password_match(self):
        if self.password != self.confirmed_password:
            raise ValueError("Mật khẩu không khớp")

        return self


class TeacherUpdateRequest(BaseModel):
    full_name: str | None = None
    department: str | None = None
    phone: str | None = Field(default=None, pattern=r"^(0|\+84)[3|5|7|8|9]\d{8}$")


class TeacherChangePasswordRequest(BaseModel):
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
