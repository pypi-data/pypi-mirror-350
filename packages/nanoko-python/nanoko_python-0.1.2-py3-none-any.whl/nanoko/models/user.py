from enum import Enum
from pydantic import BaseModel, EmailStr


class Permission(Enum):
    """Permission levels for users."""

    STUDENT = 0
    TEACHER = 1
    ADMIN = 2


class User(BaseModel):
    """User model."""

    id: int
    name: str
    display_name: str
    email: EmailStr
    permission: Permission
