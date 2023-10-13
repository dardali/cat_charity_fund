from typing import List, Dict, Any

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    spreadsheets_create,
    set_user_permissions,
    spreadsheets_update_value
)

router = APIRouter()


@router.post(
    '/',
    response_model=List[Dict[str, Any]],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    """Только для суперюзеров."""
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spread_sheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spread_sheet_id, wrapper_services)
    await spreadsheets_update_value(spread_sheet_id,
                                    projects,
                                    wrapper_services)
    return projects
