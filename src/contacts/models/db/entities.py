import uuid
from pydantic import BaseModel


class UserInDb(BaseModel):
    id: int
    username: str
    hashed_password: str
    role: str


class ContactInDb(BaseModel):
    id: uuid.UUID
    owner_id: int
    last_name: str
    first_name: str
    middle_name: str
    organisation: str
    job_title: str
    email: str
    phone_number: str
