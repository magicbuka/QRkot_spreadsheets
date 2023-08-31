from datetime import datetime
from typing import List

from app.models.base import BaseModel


def investment(
    target: BaseModel,
    sources: List[BaseModel]
) -> List[BaseModel]:
    modified = []
    for source in sources:
        amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for investment in [target, source]:
            investment.invested_amount += amount
            if investment.invested_amount == investment.full_amount:
                investment.fully_invested = True
                investment.close_date = datetime.now()
        modified.append(source)
        if target.fully_invested:
            break
    return modified
