from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseModel

DESCRIPTION = (
    'Пользователь: {user_id}, '
    'Комментарий: {comment}, '
    '{invested}'
)


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return DESCRIPTION.format(
            user_id=self.user_id[:20],
            comment=self.comment[:20],
            invested=super().__repr__()
        )
