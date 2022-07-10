import asyncio
import os

import uvloop
from dotenv import load_dotenv
from sqlalchemy import (BigInteger, Boolean, Column, String, Text, delete,
                        select)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password")
POSTGRES_SERVER_IP = os.getenv("Postgres_IP")
POSTGRES_DATABASE = os.getenv("Postgres_Events_Database")
POSTGRES_USERNAME = os.getenv("Postgres_User")

Base = declarative_base()


class UserEvents(Base):
    __tablename__ = "user_events"

    event_item_uuid = Column(String, primary_key=True)
    user_id = Column(BigInteger)
    name = Column(String)
    description = Column(Text)
    date_added = Column(String)
    event_date = Column(String)
    event_passed = Column(Boolean)

    def __repr__(self):
        returnStruct = {
            "event_item_uuid": self.event_item_uuid,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "date_added": self.date_added,
            "event_date": self.event_date,
            "event_passed": self.event_passed,
        }
        return returnStruct


class MikuEventsUtils:
    def __init__(self):
        self.self = self

    async def initTables(self):
        """Initialize the Database Tables"""
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}",
            echo=True,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def insertNewEvent(
        self,
        event_uuid: str,
        user_id: int,
        name: str,
        description: str,
        date_added: str,
        event_date: str,
        event_passed: bool,
    ):
        """Adds a new item into the DB

        Args:
            event_uuid (str): The UUID of the item
            user_id (int): The Discord ID of the user
            name (str): The name of the item
            description (str): The description of the item
            date_added (str / ISO-8601): The date the event was added
            event_date (str / ISO-8601): The date the event is held on
            event_passed (bool): Whether or not the event has passed
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )

        async with async_session() as session:
            async with session.begin():
                eventItem = UserEvents(
                    event_item_uuid=event_uuid,
                    user_id=user_id,
                    name=name,
                    description=description,
                    date_added=date_added,
                    event_date=event_date,
                    event_passed=event_passed,
                )
                session.add_all([eventItem])
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectUserEvent(self, user_id: int):
        """Selects all of the events that a user has

        Args:
            user_id (int): Discord User ID
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(UserEvents).filter(UserEvents.user_id == user_id)
                results = await session.execute(selectItem)
                return [row for row in results.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectUserEventPassed(self, user_id: int, event_passed: bool):
        """Obtains any upcoming or past events for the user

        Args:
            user_id (int): Discord user ID
            passed (bool): Whether the event has passed or not
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectUpcomingItems = (
                    select(UserEvents)
                    .filter(UserEvents.user_id == user_id)
                    .filter(UserEvents.event_passed == event_passed)
                )
                res = await session.execute(selectUpcomingItems)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def deleteOneUserEvent(self, user_id: int, event_uuid: str):
        """Deletes one event from the user

        Args:
            user_id (int): Discord User ID
            event_uuid (str): Event UUID
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectOneDelete = (
                    select(UserEvents)
                    .filter(UserEvents.user_id == user_id)
                    .filter(UserEvents.event_item_uuid == event_uuid)
                )
                itemSelected = await session.scalars(selectOneDelete)
                itemSelectedOne = itemSelected.one()
                await session.delete(itemSelectedOne)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainItemUUID(self, user_id: int, name: str):
        """Obtains the Item's UUID via its name

        Args:
            user_id (int): Discord User ID
            name (str): The name of the item
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItemUUID = (
                    select(UserEvents.event_item_uuid)
                    .filter(UserEvents.user_id == user_id)
                    .filter(UserEvents.name == name)
                )
                res = await session.execute(selectItemUUID)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainItemUUIDAuth(self, user_id: int):
        """Obtains the Item's UUID via the discord user's ID
        This is used to obtain the UUId before purging all events from the user's account

        Args:
            user_id (int): Discord User ID
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItemUUIDAuth = select(UserEvents.event_item_uuid).filter(
                    UserEvents.user_id == user_id
                )
                res = await session.execute(selectItemUUIDAuth)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def deleteAllUserEvent(self, user_id: int):
        """Deletes ALL events from the user

        Args:
            user_id (int): Discord User ID
        """
        engine = create_async_engine(
            f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:5432/{POSTGRES_DATABASE}"
        )

        async_session2 = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session2() as session2:
            async with session2.begin():
                selectAllDelete = delete(UserEvents).filter(
                    UserEvents.user_id == user_id
                )
                await session2.execute(selectAllDelete)
                await session2.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
