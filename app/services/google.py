from copy import deepcopy
from datetime import datetime as dt
from typing import Tuple
from aiogoogle import Aiogoogle

from app.core.config import settings

DATETIME = "%Y/%m/%d %H:%M:%S"
ROWS = 50
COLUMNS = 5
TITLE = 'Отчет от {}'

BODY = dict(
    properties=dict(
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
HEADER = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
SIZE_ERROR = (
    'Передано больше данных, чем размер таблицы. '
    'Передано: {rows} строк {columns} столбцов. '
    'Таблица:  {ROWS} строк {COLUMNS} столбцов.'
)


async def spreadsheets_create(
        aiogoogle: Aiogoogle,
        body=None
) -> Tuple[str, str]:
    if body is None:
        body = deepcopy(BODY)
        body['properties']['title'] = TITLE.format(
            date=dt.now().strftime(DATETIME)
        )
    service = await aiogoogle.discover('sheets', 'v4')
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
    projects_values = sorted((
        (
            project.name,
            project.close_date - project.create_date,
            project.description
        ) for project in charity_projects
    ), key=lambda object: object[1])
    header = deepcopy(HEADER)
    header[0][1] = str(dt.now().strftime(DATETIME))
    table_values = [
        *header,
        *[list(map(str, field)) for field in projects_values],
    ]
    rows = len(table_values)
    columns = len(max(header, key=len))
    if rows > ROWS or columns > COLUMNS:
        raise ValueError(
            SIZE_ERROR.format(
                rows=rows,
                columns=columns
            ),
        )
    await aiogoogle.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows}C{columns}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            },
        )
    )
