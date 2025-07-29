import json
import sys

from .__version__ import VERSION


def check_unicode_support():
    return sys.stdout.encoding.lower() == "utf-8"


def initialize_config(path):
    with open(path, "w") as file:
        config = {
            "theme": "light",
            "default_output": "table",
            "version": VERSION,
            "pretty_tree": True,
            "current_table": "tasks",
        }
        json.dump(config, file, indent=4)
        return config


def update_config(path, config):
    with open(path, "w") as file:
        json.dump(config, file, indent=4)


def get_config(path):
    with open(path, "r") as file:
        return json.load(file)
