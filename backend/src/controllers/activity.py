
import re
from peewee import fn
from src.models.activity import BaseActivity, BaseActivityIndex
from src.controllers.event import DefaultEvent as Event
from src.controllers.time_entry import DefaultTimeEntry as TimeEntry
from src.helpers.time import now_br, date_trunc_day


class DefaultActivity(BaseActivity):
    """
    Default activity object's class
    """

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

        return cls.prepare_names([dict(result) for result in query])

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
            .where(
               TimeEntry.start_time > date_trunc_day(now_br())
            ).group_by(Activity.name)
        ).dicts()

        return cls.prepare_names([dict(result) for result in query])

    @classmethod
    def load_range(cls, start_date, end_date) -> list:
        """
        Returns activities registered between a given range
        :start_date: Inital range date
        :end_date: Final range date
        """
        Activity = cls.alias()
        query = (
            Event.select(
                Activity.name,
                fn.sum(TimeEntry.duration).alias("duration"),
            )
            .join(TimeEntry, on=(Event.id == TimeEntry.event_id))
            .join(Activity, on=(Event.model_id == Activity.id))
            .where(
               (TimeEntry.start_time > start_date) &
               (TimeEntry.end_time < end_date)
            ).group_by(Activity.name)
        ).dicts()

        return cls.prepare_names([dict(result) for result in query])

    @classmethod
    def full_text_search(cls, text) -> list:
        """
        Returns today's registered activities
        """
        Activity = cls.alias()
        ActivityIndex = DefaultActivityIndex().alias()
        query = (
            Event.select(
                Activity.name,
                fn.sum(TimeEntry.duration).alias("duration"),
            )
            .join(Activity, on=(Event.model_id == Activity.id))
            .join(TimeEntry, on=(Event.id == TimeEntry.event_id))
            .join(ActivityIndex, on=(Activity.id == ActivityIndex.rowid))
            .where(ActivityIndex.match(text))
            .order_by(ActivityIndex.bm25())).dicts()

        return cls.prepare_names([dict(result) for result in query])

    @staticmethod
    def prepare_names(activity_list):
        for activity in activity_list:
            description_levels = re.split('\-|\|', activity['name'])
            main_description = description_levels[-1]
            detailed_description = (
                description_levels[1:-1]
                if len(description_levels) > 2 else
                description_levels[0:-1]
                if len(description_levels) > 1 else None
            )
            detailed_description = (
                ' '.join(map(str, detailed_description))
                if detailed_description else None
            )
            more_details = (
                description_levels[0]
                if len(description_levels) > 2 else None
            )
            activity.update(dict(
                                main_description=main_description,
                                detailed_description=detailed_description,
                                more_details=more_details)
                            )
        return activity_list


class DefaultActivityIndex(BaseActivityIndex):
    """
    Activity full text search
    """
    pass
