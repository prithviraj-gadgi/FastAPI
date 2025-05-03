import re
from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr, conint, field_validator, Field

from model.card import CardIn, CardOut


class CustomerIn(BaseModel):
    customerId: str = Field(..., description="Allowed 8–20 chars, alphanumeric/._ only, no leading/trailing or consecutive ._")
    name: str = Field(..., pattern=r"^[A-Za-z][A-Za-z\s]{1,19}$", strict=True, description="Name must start with a letter, allows only letters and spaces, total length 2 to 20")
    age: int = Field(..., ge=18, le=100)
    email: EmailStr
    phoneNo: str = Field(..., pattern=r"^\d{10}$", strict=True, description="Phone number must be exactly 10 digits")
    address: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., description="Allowed 8–20 at least one uppercase, one lowercase, one digit, one special character from this set: @$!%*?&")
    cards: Optional[List[CardIn]] = None

    @field_validator("customerId")
    @classmethod
    def validate_customer_id(cls, value: str) -> str:
        if not re.fullmatch(r"^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$", value):
            raise ValueError(
                "Invalid customerId: Allowed 8–20 chars, alphanumeric/._ only, no leading/trailing or consecutive ._")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$", value):
            raise ValueError(
                "Invalid password: Allowed 8–20 at least one uppercase, one lowercase, one digit, one special character from this set: @$!%*?&")
        return value

class CustomerOut(BaseModel):
    customerId: str
    name: str
    age: int
    email: EmailStr
    phoneNo: str
    address: str
    password: str
    cards: Optional[List[CardOut]] = None

class UpdateCustomer(BaseModel):
    customerId: Optional[str] = Field(default=None, description="Allowed 8–20 chars, alphanumeric/._ only, no leading/trailing or consecutive ._")
    name: Optional[str] = Field(default=None, pattern=r"^[A-Za-z][A-Za-z\s]{1,19}$", strict=True, description="Name must start with a letter, allows only letters and spaces, total length 2 to 20")
    age: Optional[int] = Field(default=None, ge=18, le=100)
    email: Optional[EmailStr] = None
    phoneNo: Optional[str] = Field(default=None, pattern=r"^\d{10}$", strict=True, description="Phone number must be exactly 10 digits")
    address: Optional[str] = Field(default=None, min_length=5, max_length=100)
    password: Optional[str] = Field(default=None, description="Allowed 8–20 at least one uppercase, one lowercase, one digit, one special character from this set: @$!%*?&")

    @field_validator("customerId")
    @classmethod
    def validate_customer_id(cls, value: str) -> str:
        if not re.fullmatch(r"^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$", value):
            raise ValueError(
                "Invalid customerId: Allowed 8–20 chars, alphanumeric/._ only, no leading/trailing or consecutive ._")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$", value):
            raise ValueError(
                "Invalid password: Allowed 8–20 at least one uppercase, one lowercase, one digit, one special character from this set: @$!%*?&")
        return value