from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_exists(
        obj_id: int,
        session: AsyncSession,
):
    model_object = await charity_project_crud.get(obj_id, session)
    if model_object is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Объект не существует!'
        )
    return model_object


async def check_the_opportunity_to_delete(
        project: CharityProject,
):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_the_opportunity_to_update_project(
        project: CharityProject,
        update_data: CharityProjectUpdate,
) -> CharityProject:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    if update_data.full_amount is not None:
        if project.invested_amount > update_data.full_amount:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Нельзя установить требуемую сумму меньше внесённой!'
            )
    return project


async def check_the_unique_project_name(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_the_unique_project_name_update(
        check_name: str,
        project_id: int,
        session: AsyncSession,
) -> None:
    db_project_id = await charity_project_crud.get_project_id_by_name(
        check_name, session)
    if db_project_id is not None and db_project_id != project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )
