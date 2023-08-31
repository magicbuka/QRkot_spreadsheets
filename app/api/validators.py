from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate

NAME_EXISTS_ERROR = 'Проект с таким именем уже существует!'
PROJECT_NOT_EXIST_ERROR = 'Проект {name} не найден.'
PROJECT_CLOSED_ERROR = 'Закрытый проект нельзя редактировать!'
SMALL_AMOUNT_ERROR = (
    'Нельзя установить сумму, ниже уже вложенной! '
    'Проект {project}, сумма {amount}'
)
PROJECT_DELETE_ERROR = 'В проект были внесены средства, не подлежит удалению!'


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session
    )
    if project_id is not None:
        raise HTTPException(status_code=400, detail=NAME_EXISTS_ERROR,)


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail=PROJECT_NOT_EXIST_ERROR.format(charity_project.name)
        )
    return charity_project


def check_charity_project_close(
    project: CharityProject,
) -> None:
    if project.fully_invested:
        raise HTTPException(status_code=400, detail=PROJECT_CLOSED_ERROR)


def check_invested_before_edit(
    project: CharityProject,
    project_request: CharityProjectUpdate,
) -> None:
    if (
        project_request.full_amount is not None and
        project.invested_amount > project_request.full_amount
    ):
        raise HTTPException(
            status_code=400,
            detail=SMALL_AMOUNT_ERROR.format(
                project=project.name,
                amount=project.invested_amount
            )
        )


def check_invested_before_delete(
    project: CharityProject,
) -> None:
    if project.invested_amount > 0:
        raise HTTPException(status_code=400, detail=PROJECT_DELETE_ERROR)
