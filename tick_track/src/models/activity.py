import peewee
from peewee import fn
from playhouse.sqlite_ext import FTSModel, RowIDField, SearchField
from src.models.event import Event
from src.models.time_entry import TimeEntry as TimeEntry
from src.helpers.time import date_trunc_day, now_br
from src.models.base import BaseModel
from src.models.operational_system import OperationalSystem


class Activity(BaseModel):
    """
    Defines the table fileds
    """

    id = peewee.AutoField()
    name = peewee.TextField(unique=True)
    operational_system = peewee.ForeignKeyField(OperationalSystem)

    class Meta:
        def table_function(model_cls):
            """
            Names the table according to the returned value
            """
            return "Activity"

    @classmethod
    def load_all(cls) -> list:
        """
        Returns all activities registered
        """
        Activity = cls.alias()
        query = (
            Event.select(
                Activity.name,
                fn.sum(TimeEntry.duration).alias("duration"),
            )
            .join(TimeEntry, on=(Event.id == TimeEntry.event_id))
            .join(Activity, on=(Event.model_id == Activity.id))
            .group_by(Activity.name)
        ).dicts()

        return [dict(result) for result in query]

    @classmethod
    def load_today(cls) -> list:
        """
        Returns today's registered activities
        """
        Activity = cls.alias()
        query = (
            Event.select(
                Activity.name,
                fn.sum(TimeEntry.duration).alias("duration"),
            )
            .join(TimeEntry, on=(Event.id == TimeEntry.event_id))
            .join(Activity, on=(Event.model_id == Activity.id))
            .where(TimeEntry.start_time > date_trunc_day(now_br()))
            .group_by(Activity.name)
        ).dicts()

        return [dict(result) for result in query]

    @classmethod
    def load_range(cls, start_date, end_date) -> list:
        """
        Returns activities registered between a given date range
        :start_date: Inital range date
        :end_date: Final range date
        """
        if not start_date:
            start_date = "1900-01-01"
        if not end_date:
            end_date = "3000-01-01"

        Activity = cls.alias()
        query = (
            Event.select(
                Activity.name,
                fn.sum(TimeEntry.duration).alias("duration"),
            )
            .join(TimeEntry, on=(Event.id == TimeEntry.event_id))
            .join(Activity, on=(Event.model_id == Activity.id))
            .where(
                (TimeEntry.start_time > start_date)
                & (TimeEntry.end_time < end_date)
            )
            .group_by(Activity.name)
        ).dicts()

        return [dict(result) for result in query]

    @classmethod
    def full_text_search(cls, text, start_date, end_date) -> list:
        """
        Returns full text between a given date range
        :text:
        :start_date: Inital range date
        :end_date: Final range date
        """
        if not start_date:
            start_date = "1900-01-01"
        if not end_date:
            end_date = "3000-01-01"

        Activity = cls.alias()
        ActivityIndex = ActivityIndex().alias()
        query = (
            Event.select(
                Activity.name,
                fn.sum(TimeEntry.duration).alias("duration"),
            )
            .join(Activity, on=(Event.model_id == Activity.id))
            .join(TimeEntry, on=(Event.id == TimeEntry.event_id))
            .join(ActivityIndex, on=(Activity.id == ActivityIndex.rowid))
            .where(
                (ActivityIndex.match(text))
                & (TimeEntry.start_time > start_date)
                & (TimeEntry.end_time < end_date)
            )
            .order_by(ActivityIndex.bm25())
        ).dicts()

        return [dict(result) for result in query]


class ActivityIndex(BaseModel, FTSModel):
    rowid = RowIDField()
    name = SearchField()

    class Meta:
        # Use the porter stemming algorithm to tokenize content.
        options = {"tokenize": "porter"}

        def table_function(model_cls):
            """
            Names the table according to the returned value
            """
            return "ActivityIndex"
