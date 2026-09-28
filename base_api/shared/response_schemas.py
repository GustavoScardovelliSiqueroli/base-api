from pydantic import BaseModel


class ApiResponse[T](BaseModel):
    success: bool = True
    data: T | None = None
