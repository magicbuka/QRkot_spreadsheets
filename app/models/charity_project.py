from sqlalchemy import Column, String, Text

from app.models.base import BaseModel

DESCRIPTION = (
    'Название: {name}, '
    'Описание: {description}, '
    '{invested}'
)


class CharityProject(BaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return DESCRIPTION.format(
            name=self.name[:20],
            description=self.description[:20],
            invested=super().__repr__()
        )
