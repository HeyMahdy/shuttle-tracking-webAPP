from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from Dbs.DataBaseSetting.DatabaseConfig import get_async_db
from Dbs.Models.models import MainUser
from Dbs.Schemas.modelSchemas import UserCreate
from sqlalchemy.future import select

from auth.utils import generate_password_hash


async def create_user(user_data: UserCreate, db: AsyncSession):
    """Service method to create a new user asynchronously."""
    new_user = MainUser(email = user_data.email, username = user_data.username,password = generate_password_hash(user_data.password),role=user_data.role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_users(email: str, db: AsyncSession):
    result = await db.execute(select(MainUser).where(MainUser.email == email))
    user = result.scalar_one_or_none()
    return user

async def get_role_by_email(email: str, db: AsyncSession):
    result = await db.execute(select(MainUser.role).where(MainUser.email == email))
    role = result.scalar_one_or_none()
    return role
