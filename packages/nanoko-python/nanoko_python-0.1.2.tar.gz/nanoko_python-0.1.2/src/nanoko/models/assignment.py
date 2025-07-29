from pydantic import BaseModel


class Assignment(BaseModel):
    """Assignment model for API."""

    id: int
    name: str
    description: str
    teacher_id: int


class Class(BaseModel):
    """Class model for API."""

    id: int
    name: str
    enter_code: str
    teacher_id: int


class FeedBack(BaseModel):
    """Feedback model for API."""

    comment: str
    performance: int
