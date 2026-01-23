import uuid

from pydantic import BaseModel, Field


class CreateUserSchema(BaseModel):
    login: str = Field(min_length=4)
    password: str = Field(min_length=8)


class PublicUserSchema(BaseModel):
    user_id: uuid.UUID
    login: str

    class Config:
        from_attributes = True
