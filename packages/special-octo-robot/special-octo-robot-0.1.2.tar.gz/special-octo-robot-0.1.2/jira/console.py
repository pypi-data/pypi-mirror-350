import click
import keyring

from app.config import update_config
from app.constants import config_path


def set_jira_config(config):
    if config.get("jira", None) is None:
        config["jira"] = {}
        config = set_organization_url(config=config)
        config = set_organization_email(config=config)
        set_token()

    return config


def set_organization_url(config):
    config["jira"]["url"] = click.prompt(
        "Enter Jira URL for API (Ex: 'https://<enterprise>jira.atlassian.net/')",
        type=str,
    )
    update_config(config_path, config)
    return config


def set_organization_email(config):
    config["jira"]["email"] = click.prompt("Enter oragnizational Email", type=str)

    update_config(config_path, config)
    return config


def set_token():
    token = click.prompt("Enter private API token", type=str)
    keyring.set_password("devcord", "token", token)
