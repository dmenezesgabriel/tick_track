import datetime
from peewee import fn
from src.models.base_activity import BaseActivity
from src.controllers.event import DefaultEvent as Event
from src.controllers.time_entry import DefaultTimeEntry as TimeEntry
from src.utils.time import now_br, date_trunc_day


class DefaultActivity(BaseActivity):

    @classmethod
    def load_all(cls):
        Activity = cls.alias()
        query = (
            Event.select(
                Activity.name,
                fn.sum(TimeEntry.duration),
            )
            .join(TimeEntry, on=(Event.id == TimeEntry.event_id))
            .join(Activity, on=(Event.model_id == Activity.id))
            .group_by(Activity.name)
        ).dicts()

        return [dict(result) for result in query]

    @classmethod
    def load_today(cls):
        Activity = cls.alias()
        query = (
            Event.select(
                Activity.name,
                fn.sum(TimeEntry.duration),
            )
            .join(TimeEntry, on=(Event.id == TimeEntry.event_id))
            .join(Activity, on=(Event.model_id == Activity.id))
            .where(
               TimeEntry.start_time > date_trunc_day(now_br())
            ).group_by(Activity.name)
        ).dicts()

        return [dict(result) for result in query]

    @classmethod
    def load_range(cls, start_date, end_date):
        Activity = cls.alias()
        query = (
            Event.select(
                Activity.name,
                fn.sum(TimeEntry.duration),
            )
            .join(TimeEntry, on=(Event.id == TimeEntry.event_id))
            .join(Activity, on=(Event.model_id == Activity.id))
            .where(
               (TimeEntry.start_time > start_date) & (TimeEntry.end_time < end_date)
            ).group_by(Activity.name)
        ).dicts()

        return [dict(result) for result in query]
