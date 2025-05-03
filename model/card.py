from datetime import date, datetime

from pydantic import Field, field_validator, BaseModel


class CardIn(BaseModel):
    cardNumber: str = Field(..., pattern=r"^\d{16}$", strict=True, description="Card number must be exactly 16 digits")
    cardType: str = Field(..., pattern=r"Visa|Master Card|Amex", description="Card type must be either Visa, Master Card, or Amex")
    expirationDate: date
    cvv: str = Field(..., min_length=3, max_length=3)
    nameOnCard: str = Field(..., pattern=r"^[A-Za-z][A-Za-z\s]{1,19}$", strict=True, description="Name must start with a letter, allows only letters and spaces, total length 2 to 20")

    @field_validator("expirationDate")
    @classmethod
    def validate_expiration_date(cls, value: date) -> date:
        if value < datetime.today().date():
            raise ValueError("Expiration date must be in the future")
        return value

class CardOut(BaseModel):
    cardNumber: str
    cardType: str
    expirationDate: date
    cvv: str
    nameOnCard: str