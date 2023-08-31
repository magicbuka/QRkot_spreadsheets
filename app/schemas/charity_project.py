from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    invested_amount: int = 0


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = 1


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: datetime = None

    class Config:
        orm_mode = True
