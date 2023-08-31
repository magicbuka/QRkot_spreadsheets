from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.services.google import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value
)

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        aiogoogle: Aiogoogle = Depends(get_service),
):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id, spreadsheet_url = await spreadsheets_create(aiogoogle)
    await set_user_permissions(spreadsheet_id, aiogoogle)
    try:
        await spreadsheets_update_value(
            spreadsheet_id,
            projects,
            aiogoogle
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    return spreadsheet_url
