from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_close,
    check_charity_project_exists,
    check_invested_before_delete,
    check_invested_before_edit,
    check_name_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services import investment

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDB]:
    return await charity_project_crud.get_all(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_charity_project(
    new_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    await check_name_duplicate(new_project.name, session)
    new_project = await charity_project_crud.create(
        new_project,
        session,
        commit=False
    )
    session.add_all(
        investment(
            new_project, await donation_crud.get_opened(session)
        )
    )
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    project = await check_charity_project_exists(project_id, session)
    check_charity_project_close(project)
    check_invested_before_edit(project, obj_in)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    return await charity_project_crud.update(
        project,
        obj_in,
        session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    project = await check_charity_project_exists(project_id, session)
    check_invested_before_delete(project)
    return await charity_project_crud.remove(project, session)
