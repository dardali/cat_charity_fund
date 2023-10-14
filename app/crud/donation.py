from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import FULLY_INVESTED_FALSE
from app.crud.base import CRUDBase
from app.models import Donation, User, CharityProject


class CRUDDonation(CRUDBase):

    async def distribute_funds(self, db_donation, projects):
        for project in projects:
            if db_donation.invested_amount >= db_donation.full_amount:
                break

            funds_to_fill = db_donation.full_amount - db_donation.invested_amount
            fill = min(funds_to_fill, project.full_amount - project.invested_amount)

            db_donation.invested_amount += fill
            project.invested_amount += fill

            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()

            if db_donation.invested_amount == db_donation.full_amount:
                db_donation.fully_invested = True
                db_donation.close_date = datetime.now()

    async def create_donation(self, obj_in, user: User, session: AsyncSession):
        obj_in_data = obj_in.dict()
        obj_in_data['create_date'] = datetime.now()
        obj_in_data['user_id'] = user.id
        obj_in_data['invested_amount'] = 0
        db_donation = self.model(**obj_in_data)

        projects = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested == FULLY_INVESTED_FALSE)
            .order_by(CharityProject.create_date)
        )
        projects = projects.scalars().all()

        await self.distribute_funds(db_donation, projects)

        session.add(db_donation)
        await session.commit()
        await session.refresh(db_donation)
        return db_donation

    async def get_my(self, user: User, session: AsyncSession) -> List[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
