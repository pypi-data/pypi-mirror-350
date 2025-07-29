import json
import sys

from .__version__ import VERSION


def check_unicode_support():
    return sys.stdout.encoding.lower() in ("utf-8", "utf-16", "utf-32")


def initialize_config(
    path,
    theme="light",
    version=VERSION,
    pretty_tree=True,
    current_table="tasks",
    jira={},
    current_task=-1,
    **kwargs,
):
    with open(path, "w+") as file:
        config = {
            "theme": theme,
            "version": version,
            "pretty_tree": pretty_tree,
            "current_table": current_table,
            "jira": jira,
            "current_task": current_task,
        }
        json.dump(config, file, indent=4)
        return config


def update_config(path, config):
    initialize_config(path, **config)


def get_config(path):
    with open(path, "r") as file:
        return json.load(file)
