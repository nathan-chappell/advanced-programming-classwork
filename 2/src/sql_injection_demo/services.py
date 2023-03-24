from typing import Any, Literal

import asyncio

from sanic.log import logger

from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from sql_injection_demo.models import User

db_engine = create_async_engine("sqlite+aiosqlite://")
async_session = async_sessionmaker(db_engine)


async def init_db():
    async with db_engine.connect() as connection:
        await connection.execute(
            text("""CREATE TABLE IF NOT EXISTS user(username text primary key, password text, secrets text nullable)""")
        )


asyncio.get_event_loop().run_until_complete(init_db())


class UserService:
    async def get_user(self, username: str, password: str) -> User | None:
        async with db_engine.connect() as connection:
            hashed_password = User.hash_password(password)
            results = list(
                await connection.execute(
                    text(f"""SELECT secrets FROM user WHERE username = '{username}' AND password = '{hashed_password}'""")
                )
            )
            if len(results) == 0:
                return None
            else:
                return User(username=username, password=hashed_password, secrets=results[0][0])

    async def get_secrets(self, username: str, password: str) -> Any | None:
        async with db_engine.connect() as connection:
            hashed_password = User.hash_password(password)
            results = list(
                await connection.execute(
                    text(f"""SELECT secrets FROM user WHERE username = '{username}' AND password = '{hashed_password}'""")
                )
            )
            if len(results) == 0:
                return None
            return [list(r) for r in results]

    async def user_exists(self, username: str) -> bool:
        async with db_engine.connect() as connection:
            results = list(await connection.execute(text(f"""SELECT count(*) FROM user WHERE username = '{username}'""")))
            logger.info(f"{username=} {results=}")
            return results[0][0] > 0

    async def upsert_user(self, username: str, password: str, secrets: str | None) -> Literal["added", "updated"]:
        async with async_session() as session:
            user = await session.get(User, username)
            if user is None:
                result = "added"
                user = User(username=username, password=User.hash_password(password), secrets=secrets)
            else:
                result = "updated"
                user.password = User.hash_password(password)
                user.secrets = secrets
            session.add(user)
            await session.commit()
        return result
