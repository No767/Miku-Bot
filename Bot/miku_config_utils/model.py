from sqlalchemy import BigInteger, Boolean, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class MikuConfig(Base):
    __tablename__ = "miku_config"

    guild_id = Column(BigInteger, primary_key=True)
    scheduled_events_reminders = Column(Boolean)

    def __iter__(self):
        yield "guild_id", self.guild_id
        yield "scheduled_events_reminders", self.scheduled_events_reminders

    def __repr__(self):
        return f"MikuConfig(guild_id={self.guild_id}, scheduled_events_reminders={self.scheduled_events_reminders})"
