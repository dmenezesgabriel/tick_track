import os
from importlib import util
import sys
import logging


# Map migrations folder
dir_path = os.path.dirname(__file__)
migrations_path = os.path.join(dir_path, "migrations")
path = migrations_path

# Look for migrations on migrations folder
migrations = sorted(
    filter(
        lambda file_name: file_name.endswith(".py"), os.listdir(path)
    )
)

# Apply migrations found
for migration in migrations:
    print(f"migration {migration} executed")
    migration_path = os.path.join(
        os.path.dirname(__file__), "migrations", migration)
    spec = util.spec_from_file_location(migration, migration_path)
    migration_import = util.module_from_spec(spec)
    spec.loader.exec_module(migration_import)
    migration_import.apply()
