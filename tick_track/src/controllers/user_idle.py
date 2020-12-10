import logging
import asyncio
import src.helpers.platform as platform_helper


_logger = logging.getLogger('InactivityController')

_should_run = True
user_idle_seconds = 0


def stop():
    _logger.info('Stopping inactivity check')
    global _should_run
    _should_run = False


async def run():
    global user_idle_seconds
    _logger.info('Starting Inactivity checking at background')
    os_name = platform_helper.get_os_name()
    platform_helper.import_os_helpers(os_name)

    monitor = platform_helper.os_inactivity_monitor(os_name)

    # start monitoring
    try:
        monitor.start()
        while True:
            if not _should_run:
                break

            idle_seconds = monitor.get_idle_seconds()
            user_idle_seconds = idle_seconds
            await asyncio.sleep(1)

        # close monitor when finished
        monitor.close()
    except Exception as error:
        _logger.error(
            'Error on running InactivityController. Error: %s', error)
