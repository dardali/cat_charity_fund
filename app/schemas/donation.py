from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.core.utils import EXAMPLE_VALUE


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(..., example=EXAMPLE_VALUE)
    comment: Optional[str] = Field(
        None,
        title='Комментарий к пожертвованию',
        example='На корм кошечкам',
    )


class DonationUpdate(DonationBase):
    pass


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool

    class Config:
        orm_mode = True


class DonationUserDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
