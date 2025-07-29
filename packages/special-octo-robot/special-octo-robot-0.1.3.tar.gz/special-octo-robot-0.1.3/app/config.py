import json

from click import echo
from click import style

from .__version__ import VERSION


def check_unicode_support():
    try:
        echo(
            style(
                text="✔️ Unicode Supported",
                fg="yellow",
            ),
        )
        return True
    except UnicodeEncodeError:
        echo(
            style(
                text="Unicode Unsupported",
                fg="yellow",
            ),
        )
        return False


def initialize_config(path):
    with open(path, "w") as file:
        config = {
            "theme": "light",
            "default_output": "table",
            "unicode": check_unicode_support(),
            "version": VERSION,
            "pretty_tree": True,
        }
        json.dump(config, file, indent=4)
        return config


def update_config(path, config):
    with open(path, "w") as file:
        json.dump(config, file, indent=4)


def get_config(path):
    with open(path, "r") as file:
        return json.load(file)
