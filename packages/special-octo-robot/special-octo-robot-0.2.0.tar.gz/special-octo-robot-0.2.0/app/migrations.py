import sqlite3

from packaging.version import Version

from .constants import db_path
from app.__version__ import VERSION
from app.config import update_config
from app.constants import config_path


migration_list = [
    ("0.0.8", """ALTER TABLE tasks ADD COLUMN subtasks INTEGER DEFAULT 0;"""),
    ("0.0.12", """CREATE INDEX title on tasks(title);"""),
]


def run_migrations(previous_version):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    previous_version = Version(previous_version)
    for migration in migration_list:
        if Version(migration[0]) > previous_version:
            cur.execute(migration[1])
            conn.commit()
    conn.close()


def update_version(config):
    if config["version"] != VERSION:
        run_migrations(previous_version=config["version"])
        config["version"] = VERSION
        update_config(config_path, config=config)
