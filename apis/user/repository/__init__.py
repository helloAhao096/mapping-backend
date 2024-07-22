import json

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from db.models import User
from utils.datatime_helper import str_to_datatime, datatime_to_str, datetime


class UserServeries:


    @staticmethod
    async def create_user(async_session: AsyncSession, **kwargs):
        new_user = User(**kwargs)
        async_session.add(new_user)
        await async_session.commit()
        return new_user


    @staticmethod
    async def select_by_user_email(async_session: AsyncSession, **kwargs):
        user = User(**kwargs)
        print(user.email)
        query = select(User).where(User.email == user.email, User.status == "ACTIVE")
        _result = await async_session.execute(query)
        print(_result)
        user_result = _result.first()[0]
        print(user_result,"user")
        return user_result

    @staticmethod
    async def select_user_info(async_session: AsyncSession, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        print(kwargs)
        user = User(**kwargs)
        print(user,'userxxx')
        query = None
        for key, value in kwargs.items():
            query = select(User).where(getattr(User, key) == value)
        _result = await async_session.execute(query)
        user_result = _result.first()[0]
        print(user_result, "user")
        # return json.dumps(user_result.to_dict(), ensure_ascii=False, indent=4)
        return user_result.to_dict()

    @staticmethod
    async def email_signup(async_session: AsyncSession, email):
        create_user = User(email=email)
        async_session.add(create_user)
        await async_session.commit()
        return create_user