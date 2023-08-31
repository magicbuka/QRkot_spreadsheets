from datetime import datetime as dt
from typing import Tuple
from aiogoogle import Aiogoogle

from app.core.config import settings

DATETIME = "%Y/%m/%d %H:%M:%S"
ROWS = 50
COLUMNS = 5


async def spreadsheets_create(
        aiogoogle: Aiogoogle
) -> Tuple[str, str]:
    service = await aiogoogle.discover('sheets', 'v4')
    body = dict(
        properties=dict(
            title=f'Отчет от {dt.now().strftime(DATETIME)}',
            locale='ru_RU',
        ),
        sheets=[dict(properties=dict(
            sheetType='GRID',
            sheetId=0,
            title='Лист1',
            gridProperties=dict(
                rowCount=ROWS,
                columnCount=COLUMNS,
            )
        ))]
    )
    response = await aiogoogle.as_service_account(
        service.spreadsheets.create(json=body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
    spreadsheet_id: str,
    aiogoogle: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    service = await aiogoogle.discover('drive', 'v3')
    await aiogoogle.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    charity_projects: list,
    aiogoogle: Aiogoogle
) -> None:
    service = await aiogoogle.discover('sheets', 'v4')
    values = [
        ['Отчет от', dt.now().strftime(DATETIME)],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in charity_projects:
        row = [
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description)
        ]
        values.append(row)
    await aiogoogle.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': values
            },
        )
    )
