from typing import Optional
from pydantic import BaseModel, EmailStr, constr

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr  # 使用 EmailStr 验证邮箱格式
    password: constr(min_length=6)  # 密码最小长度为6
    identity: Optional[str] = None  # 设置为可选字段

class LoginRequest(BaseModel):
    email: EmailStr  # 使用 EmailStr 验证邮箱格式
    password: constr(min_length=6)  # 密码最小长度为6