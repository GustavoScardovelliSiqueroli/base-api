import uuid

from pydantic import BaseModel


class PublicUserSchema(BaseModel):
    user_id: uuid.UUID
    login: str

    class Config:
        from_attributes = True
