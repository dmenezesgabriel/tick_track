from src.models.base_activity import BaseActivity
from src.controllers.event import DefaultEvent as Event
from src.controllers.time_entry import DefaultTimeEntry as TimeEntry


class DefaultActivity(BaseActivity):

    @classmethod
    def load_activities(cls):
        Activity = cls.alias()
        query = (
            Event.select(
                Activity.name,
                TimeEntry.start_time,
                TimeEntry.end_time,
                TimeEntry.duration,
            )
            .join(TimeEntry, on=(Event.id == TimeEntry.event_id))
            .join(Activity, on=(Event.model_id == Activity.id))
        ).dicts()

        return [dict(result) for result in query]
