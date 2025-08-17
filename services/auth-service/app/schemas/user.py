# BaseModel - is a class from the Pydantic library. If a class inherits from BaseModel, it can be used to define data models with validations
# Field - is used to define metadata for the fields in the Pydantic models
# EmailStr - is a Pydantic type for validating email addresses
# ConfigDict - is used to configure behavior of model classes
from pydantic import BaseModel, Field, EmailStr, ConfigDict

# Annotated is used to add metadata to fields in Pydantic models "Annotated[type, Field(meta data)]"
from typing import Annotated, Optional


class BaseUser(BaseModel):
    id: int
    name: Annotated[str, Field(min_length=2, max_length=30, examples=["Iqra Afzal"])]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["iqra"])]
    email: Annotated[EmailStr, Field(examples=["iqra.afzal@gmail.com"])]
    role: Annotated[str, Field(examples=["hospital_professional"])]
    model_config = ConfigDict(from_attributes=True)
    

class CreateUser(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=30, examples=["Iqra Afzal"])]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["iqra"])]
    email: Annotated[EmailStr, Field(examples=["iqra.afzal@gmail.com"])]
    role: Annotated[str, Field(examples=["hospital_professional"])]
    password: Annotated[str, Field(min_length=8, max_length=128, examples=["password123"])]

class CreateUserInternal(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=30, examples=["Iqra Afzal"])]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["iqra"])]
    email: Annotated[EmailStr, Field(examples=["iqra.afzal@gmail.com"])]
    role: Annotated[str, Field(examples=["hospital_professional"])]
    password_hash: Annotated[str, Field(min_length=8, max_length=128)]

class UpdateUser(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=30, examples=["Iqra Afzal"])
    username: Optional[str] = Field(default=None, min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["iqra"])
    email: Optional[str] = Field(default=None, examples=["iqra.afzal@gmail.com"])
