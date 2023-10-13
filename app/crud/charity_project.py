from datetime import datetime
from typing import Optional, List, Dict

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import FULLY_INVESTED_TRUE, FULLY_INVESTED_FALSE
from app.crud.base import CRUDBase
from app.models import CharityProject, Donation
from app.schemas.charity_project import CharityProjectDB


class CRUDCharityProject(CRUDBase):

    async def calculate(
            self,
            db_project,
            donations
    ):
        if donations:
            for donation in donations:
                project_invested = db_project.invested_amount
                fill = db_project.full_amount - db_project.invested_amount
                funds = donation.full_amount - donation.invested_amount

                if fill >= funds:
                    db_project.invested_amount = project_invested + funds
                    if db_project.invested_amount == db_project.full_amount:
                        db_project.fully_invested = True
                        db_project.close_date = datetime.now()
                    donation.invested_amount = donation.full_amount
                    donation.fully_invested = True
                    donation.close_date = datetime.now()
                    continue
                elif fill < funds:
                    donation.invested_amount += fill
                    db_project.invested_amount = db_project.full_amount
                    db_project.fully_invested = True
                    db_project.close_date = datetime.now()
                    break
        return db_project

    async def create_project(
            self,
            obj_in,
            session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        obj_in_data['create_date'] = datetime.now()
        obj_in_data['invested_amount'] = 0
        obj_in_data['close_date'] = None
        db_project = self.model(**obj_in_data)

        donations = await session.execute(
            select(Donation)
            .where(Donation.fully_invested == FULLY_INVESTED_FALSE)
            .order_by(Donation.create_date)
        )
        donations = donations.scalars().all()

        db_project = await self.calculate(db_project, donations)

        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
        return db_project

    async def update_project(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if db_obj.invested_amount == db_obj.full_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[Dict[str, int]]:
        result = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested == FULLY_INVESTED_TRUE)
            .order_by(
                (CharityProject.close_date - CharityProject.create_date).asc()
            )
        )
        projects = result.scalars().all()

        projects_models = [CharityProjectDB.from_orm(project) for project in
                           projects]

        projects_dicts = [project_model.dict() for project_model in
                          projects_models]

        return projects_dicts


charity_project_crud = CRUDCharityProject(CharityProject)
