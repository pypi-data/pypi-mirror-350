from package.app import models
import logging
from sqlalchemy.sql import select, exists
from sqlalchemy.orm import load_only
from .base import BaseManager


logger = logging.getLogger(__name__)


class UserManager(BaseManager):
    MODEL = models.UsersModel

    async def get_all(self):
        db_users = select(models.UsersModel).options(
            load_only(
                models.UsersModel.id,
                models.UsersModel.display_name,
                models.UsersModel.email,
                models.UsersModel.phone,
                models.UsersModel.image,
                models.UsersModel.created_at,
                models.UsersModel.is_email_verified,
                models.UsersModel.is_phone_verified,
                models.UsersModel.is_superuser,
            )
        )
        return db_users

    async def check_login_credentials_and_get_id(self, email, password):
        user_q = (
            select(models.UsersModel)
            .options(
                load_only(
                    models.UsersModel.id,
                    models.UsersModel.email,
                    models.UsersModel.password,
                )
            )
            .where(models.UsersModel.email == email)
        )
        user_q = await self.db.scalars(user_q)
        user = user_q.first()
        if user and user.password == password:
            return user.id
        return False

    async def check_if_user_email_exists(self, email):
        return await self.db.scalar(
            exists().where(models.UsersModel.email == email).select()
        )

    async def check_if_user_phone_exists(self, phone):
        return await self.db.scalar(
            exists().where(models.UsersModel.phone == phone).select()
        )
