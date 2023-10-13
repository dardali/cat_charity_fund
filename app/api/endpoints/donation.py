from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationDB, DonationCreate, DonationUserDB

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_reservations(
        session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    return await donation_crud.create_donation(
        donation, user, session
    )


@router.get(
    '/my',
    response_model=List[DonationUserDB],
)
async def get_all_reservations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_my(user=user, session=session)
