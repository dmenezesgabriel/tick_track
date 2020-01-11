import datetime
import logging
import sys
import time
from src.controllers.activity import DefaultActivity as Activity
from src.controllers.event import DefaultEvent as Events
from src.controllers.operational_system import (
    DefaultOperationalSystem as OperationalSystem
)
from src.controllers.time_entry import DefaultTimeEntry as TimeEntry
import src.utils.platform as platform_utils
from src.utils.time import now_br, timestamptz_to_text


_logger = logging.getLogger("InspectorController")
_os_name = platform_utils.get_os_name()
_current_os = None


def load_os():
    """Check if os already exists, if not, create it and load the object"""
    os_name = _os_name
    OperationalSystem.get_or_create(name=os_name)
    current_os = (
        OperationalSystem.get(OperationalSystem.name == os_name).get()
    )
    return current_os


def import_os_utils():
    """Import operational system utils"""

    # Define current_os
    global _current_os
    _current_os = load_os()

    # Import current_os
    _logger.info(f"Importing current operational system: {_current_os}")
    _current_os.import_os_utils()


def get_current_window():
    """Returm current window name"""
    return _current_os.get_active_window()


def run():
    """Run and inspect window changing"""
    _logger.info(f"Running Inspector")
    import_os_utils()

    try:
        previous_window_name = None
        activity = None
        previous_start_time = None
        previous_end_time = None

        # Current window name
        current_window_name = get_current_window()
        start_time = timestamptz_to_text(now_br())

        while True:
            current_window_name = get_current_window()
            if previous_window_name != current_window_name:
                previous_end_time = timestamptz_to_text(now_br())

                # Create event
                query = Activity.select().where(
                    Activity.name == previous_window_name)
                if query.exists() and previous_start_time is not None:
                    activity = (
                        Activity.get(Activity.name == previous_window_name)
                    )
                    event = Events.create(
                        name="status_change",
                        model="activity",
                        model_id=str(activity.id),
                        created_at=timestamptz_to_text(now_br())
                    )

                    # Create a time entry for the events
                    event = (
                        Events.select().order_by(Events.id.desc()).get()
                    )
                    time_entry = TimeEntry.create(
                        model="event",
                        model_id=str(event.id),
                        start_time=previous_start_time,
                        end_time=previous_end_time
                    )

                # Create activity
                if current_window_name is not None:
                    activity = Activity.get_or_create(
                        name=current_window_name,
                        operational_system=_current_os
                    )
                    _logger.info(f"Current window name: {current_window_name}")
                    start_time = timestamptz_to_text(now_br())
                previous_window_name = current_window_name

            # Previows window name
            previous_start_time = start_time

            # Take a break
            time.sleep(1)

    except KeyboardInterrupt:

        # Check if window name already exists in database
        query = Activity.select().where(
            Activity.name == previous_window_name)
        if not query.exists():
            activity = Activity.get_or_create(
                name=current_window_name,
                operational_system=_current_os
            )
        else:
            activity = (
                Activity.get(Activity.name == current_window_name)
            )

            # Create event
            event = Events.create(
                name="status_change",
                model="activity",
                model_id=str(activity.id),
                created_at=timestamptz_to_text(now_br())
            )
            # Create a time entry for the events
            event = (
                Events.select().order_by(Events.id.desc()).get()
            )
            time_entry = TimeEntry.create(
                model="event",
                model_id=str(event.id),
                start_time=start_time,
                end_time=timestamptz_to_text(now_br())
            )

            # Take a break
            time.sleep(1)

        _logger.info("Program execution cancelled by the user")
        sys.exit()
