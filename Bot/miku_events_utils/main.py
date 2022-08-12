import asyncio

import uvloop
from sqlalchemy import (BigInteger, Boolean, Column, String, Text, delete,
                        select, update)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

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

    def __iter__(self):
        yield "event_item_uuid", self.event_item_uuid
        yield "user_id", self.user_id
        yield "name", self.name
        yield "description", self.description
        yield "date_added", self.date_added
        yield "event_date", self.event_date
        yield "event_passed", self.event_passed

    def __repr__(self):
        return f"UserEvents(event_item_uuid={self.event_item_uuid}, user_id={self.user_id}, name={self.name}, description={self.description}, date_added={self.date_added}, event_date={self.event_date}, event_passed={self.event_passed})"


class MikuEventsUtils:
    def __init__(self):
        self.self = self

    async def initTables(self, uri: str):
        """Initialize the Database Tables

        Args:
            uri (str): Connection URI
        """
        engine = create_async_engine(
            uri,
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
        uri: str,
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
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

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

    async def selectUserEvent(self, user_id: int, uri: str):
        """Selects all of the events that a user has

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = select(UserEvents).filter(UserEvents.user_id == user_id)
                results = await session.execute(selectItem)
                return [row for row in results.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def selectUserEventPassed(self, user_id: int, event_passed: bool, uri: str):
        """Obtains any upcoming or past events for the user

        Args:
            user_id (int): Discord user ID
            passed (bool): Whether the event has passed or not
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

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

    async def deleteOneUserEvent(self, user_id: int, event_uuid: str, uri: str):
        """Deletes one event from the user

        Args:
            user_id (int): Discord User ID
            event_uuid (str): Event UUID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

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

    async def obtainItemUUID(self, user_id: int, name: str, uri: str):
        """Obtains the Item's UUID via its name

        Args:
            user_id (int): Discord User ID
            name (str): The name of the item
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

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

    async def obtainItemUUIDAuth(self, user_id: int, uri: str):
        """Obtains the Item's UUID via the discord user's ID
        This is used to obtain the UUId before purging all events from the user's account

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

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

    async def deleteAllUserEvent(self, user_id: int, uri: str):
        """Deletes ALL events from the user

        Args:
            user_id (int): Discord User ID
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

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

    async def obtainEventsBool(self, event_passed: bool, uri: str):
        """Only gets the events from the db that have not been passed yet

        Args:
            event_passed (bool): Whether the event has been passed or not (Use false)
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectAllEventsBool = select(UserEvents).filter(
                    UserEvents.event_passed == event_passed
                )
                res = await session.execute(selectAllEventsBool)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def setEventPassed(self, uuid: str, event_passed: bool, uri: str):
        """Basically sets an event as passed

        Args:
            uuid (str): The uuid of the item
            event_passed (bool): Whether the event has passed or not
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectEventsToPass = update(
                    UserEvents, values={UserEvents.event_passed: event_passed}
                ).filter(UserEvents.event_item_uuid == uuid)
                await session.execute(selectEventsToPass)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainEventsName(self, user_id: int, name: str, uri: str):
        """Obtains the event from the given name

        Args:
            user_id (int): Discord user ID
            name (str): The name of the event to get
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                selectItem = (
                    select(UserEvents)
                    .filter(UserEvents.user_id == user_id)
                    .filter(UserEvents.name == name)
                )
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def updateEvent(self, user_id: int, uuid: str, event_date: str, uri: str):
        """Updates the event based on the uuid of the item

        Args:
            user_id (int): Discord user ID
            uuid (str): The event item's UUID
            event_date (str / ISO-8601): The new date and time of the event
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            async with session.begin():
                updateEvent = (
                    update(UserEvents, values={UserEvents.event_date: event_date})
                    .where(UserEvents.event_item_uuid == uuid)
                    .where(UserEvents.user_id == user_id)
                )
                await session.execute(updateEvent)
                await session.commit()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    async def obtainItemUUID(self, user_id: int, name: str, uri: str):
        """Used to only obtain the UUID of an item. Mainly used for auth purposes

        Args:
            user_id (int): Discord User ID
            name (str): Name of the item
            uri (str): Connection URI
        """
        engine = create_async_engine(uri)

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
