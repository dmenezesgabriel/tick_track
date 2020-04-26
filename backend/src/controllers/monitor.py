import logging
import traceback
import asyncio
import src.helpers.platform as platform_helper
import src.helpers.time as time_helper
from src.controllers.activity import DefaultActivity as Activity
from src.controllers.activity import DefaultActivityIndex as ActivityIndex
from src.controllers.event import DefaultEvent as Event
from src.controllers.time_entry import DefaultTimeEntry as TimeEntry
from src.controllers.operational_system import (
    DefaultOperationalSystem as OperationalSystem
)
from src.controllers import user_idle as user_idle_controller


_logger = logging.getLogger('WindowController')

_should_run = True


def stop():
    _logger.info("Stopping monitor")
    global _should_run
    _should_run = False


async def run():
    """
    Get and register window changes
    """
    _logger.info('Starting monitoring activities at background')

    os_name = platform_helper.get_os_name()
    platform_helper.import_os_helpers(os_name)

    os_created = OperationalSystem.get_or_create(name=os_name)
    os_object = os_created[0]

    previous_active_window_name = None
    previous_activity_start = None
    previous_event = None

    try:
        while _should_run:
            if user_idle_controller.user_idle_seconds > 60:
                active_window_name = "user_idle"
            else:
                active_window_name = (
                    platform_helper.os_get_active_window(os_name))
            active_window_start = time_helper.now_br()

            if active_window_name != previous_active_window_name:
                # Create previous activity time entry
                if previous_activity_start:
                    duration = (
                        (active_window_start - previous_activity_start)
                        .total_seconds())

                    TimeEntry.create(
                        event=previous_event,
                        start_time=previous_activity_start,
                        end_time=active_window_start,
                        duration=duration
                    )

                # Create activity
                activity = Activity.get_or_create(
                    name=active_window_name,
                    operational_system=os_object
                )

                if activity[1]:
                    # Create activity index
                    ActivityIndex.create(
                        rowid=activity[0].id,
                        name=activity[0].name
                    )

                # Create event
                event = Event.create(
                    name="window_changed",
                    model="activity",
                    model_id=activity[0].id,
                    created_at=time_helper.now_br(),
                    payload={"activity_name": activity[0].name}
                )

                previous_activity_start = active_window_start
                previous_active_window_name = active_window_name
                previous_event = event

            # Take a break
            await asyncio.sleep(1)

    except Exception:
        _logger.error('Error on run. Error: %s', traceback.format_exc())

    finally:
        # Create previous activity time entry
        if previous_activity_start:
            duration = (
                (active_window_start - previous_activity_start)
                .total_seconds())

            TimeEntry.create(
                event=previous_event,
                start_time=previous_activity_start,
                end_time=active_window_start,
                duration=duration
            )
