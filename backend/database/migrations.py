import datetime
import json
import logging
import os
from importlib import util
import pytz


logging.basicConfig(
    format='[%(asctime)s] (%(levelname)s) %(name)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

_logger = logging.getLogger("Migrator")


def now():
    """
    Returns UTC timestamp with time zone
    """
    return pytz.UTC.localize(datetime.datetime.utcnow())


def now_br():
    """
    Returns America - São Paulo timestamp with time zone
    """
    return now().astimezone(pytz.timezone("America/Sao_Paulo"))


def write_json(data, file_path):
    """
    Write data to json.
    :data: json structured data
    :file_path: file path string description
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def main():
    """
    If migrations at migrations folder not applied, apply them.
    """

    # Paths
    DIR_PATH = os.path.dirname(__file__)
    MIGRATIONS_PATH = os.path.join(DIR_PATH, 'migrations')
    MIGRATIONS_EXECUTION_PATH = os.path.join(
        DIR_PATH, 'migrations', 'migrations_execution.json')

    # Environment to migrate
    environment = os.getenv('ENVIRONMENT')

    # Verify already applied migrations
    with open(MIGRATIONS_EXECUTION_PATH) as json_file:
        data = json.load(json_file)

        temp = data['executed']

        migrated_list = (
            [migration_done.get("name", None)for migration_done in temp
             if environment in migration_done.get("environment", None)]
        )

    # Look for migrations at migrations folder
    migrations = sorted(
        filter(
            lambda file_name: file_name.endswith('.py'),
            os.listdir(MIGRATIONS_PATH)
        )
    )

    # Apply migrations found
    for migration in migrations:

        # If migration already applied skip
        if migration in migrated_list:
            _logger.warning('Migration %s already applied', migration)
            continue

        migration_path = os.path.join(
            os.path.dirname(__file__), 'migrations', migration)
        spec = util.spec_from_file_location(migration, migration_path)
        migration_import = util.module_from_spec(spec)
        spec.loader.exec_module(migration_import)

        try:
            migration_import.apply()
            _logger.info('migration %s executed', migration)

            migrated = {
                "name": migration,
                "date": str(now_br()),
                "environment": environment
            }

            temp.append(migrated)

        except Exception as error:
            _logger.error('migration failed. Error: %s', error)

    write_json(data, MIGRATIONS_EXECUTION_PATH)


if __name__ == '__main__':
    main()
