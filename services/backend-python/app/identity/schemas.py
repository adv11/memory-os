import uuid

from pydantic import BaseModel


class CurrentUserResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: str

    model_config = {"from_attributes": True}
