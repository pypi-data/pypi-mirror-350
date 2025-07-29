import os

import click

from app import application
from app.config import check_unicode_support
from app.config import get_config
from app.config import initialize_config
from app.config import update_config
from app.console import print_legend
from app.console import print_tables
from app.console import print_tasks
from app.constants import config_path
from app.constants import db_path
from app.constants import path
from app.database import initialize
from app.migrations import update_version
from app.utility import convert_to_db_date
from app.utility import fuzzy_search_task
from app.utility import sanitize_table_name
from jira.application import update_issues
from jira.console import set_jira_config
from jira.console import set_organization_email
from jira.console import set_organization_url
from jira.console import set_token

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """
    Devcord is a CLI tool for developers to help them with their daily tasks.
    """
    ctx.ensure_object(dict)
    if not path:
        click.echo(
            click.style(
                "Error: Could not find the path to the database, raise an issue with the developers.",
                fg="red",
            ),
        )
        ctx.abort()
        return

    # db_path as well as config_path can only be set if path is not None
    if not os.path.exists(db_path):
        os.makedirs(path, exist_ok=True)
        initialize("tasks")
    if not os.path.exists(config_path):
        ctx.obj["config"] = initialize_config(config_path)
    else:
        ctx.obj["config"] = get_config(config_path)

    ctx.obj["config"]["unicode"] = check_unicode_support()
    update_version(ctx.obj["config"])


@cli.command()
@click.pass_context
@click.option("-l", "--list", is_flag=True, help="List all the tasks")
@click.option("-a", "--add", help="Add a new task", type=str)
@click.option("-d", "--desc", is_flag=True, help="Add a description to a task")
@click.option("-p", "--priority", help="Set the priority of a task", type=int)
@click.option("-t", "--today", is_flag=True, help="Perform for all the tasks for today")
@click.option(
    "-w",
    "--week",
    is_flag=True,
    help="Perform for all the tasks for this week",
)
@click.option(
    "-dd",
    "--deadline",
    help='Set the deadline of a task, date format: "dd/mm/yyyy/"',
    type=str,
)
@click.option(
    "-i",
    "--inprogress",
    is_flag=True,
    help="Perform for all the tasks that are in progress",
)
@click.option(
    "-c",
    "--completed",
    is_flag=True,
    help="Perform for all the tasks that are completed",
)
@click.option(
    "-pd",
    "--pending",
    is_flag=True,
    help="Perform for all the tasks that are pending",
)
@click.option(
    "-lb",
    "--label",
    help="Perform for all the tasks with a specific label",
    type=str,
)
@click.option("-o", "--output", help="Specify Output Format", type=str)
@click.option("--path", help="Specify Output File", type=str)
@click.option("-st", "--subtask", is_flag=True, help="List or add subtasks")
def tasks(
    ctx,
    list=None,
    add=None,
    desc=None,
    priority=None,
    today=False,
    week=False,
    deadline=None,
    inprogress=None,
    completed=None,
    pending=None,
    label=None,
    output=None,
    path=None,
    subtask=False,
):
    """
    Create and List tasks.
    """

    if deadline:
        try:
            deadline = convert_to_db_date(deadline)
        except ValueError:
            click.echo(
                click.style(
                    'Error: Invalid date format, please use "dd/mm/yyyy".',
                    fg="red",
                ),
            )
            click.echo('Example: "01/01/2020"')
            return

    if list:
        task_list = application.list_tasks(
            priority=priority,
            today=today,
            week=week,
            inprogress=inprogress,
            completed=completed,
            pending=pending,
            label=label,
            subtasks=subtask,
        )

        if task_list:
            print_tasks(
                task_list,
                output,
                path,
                ctx.obj["config"]["unicode"] is False,
                subtask,
                "Tasks",
                ctx.obj["config"]["pretty_tree"],
            )

    elif add:
        parent = None
        description = "No given description"
        if desc:
            description = click.edit()
        if subtask:
            parent = fuzzy_search_task()
            if parent is None:
                click.echo(
                    click.style(
                        "Error: Parent task does not exist.",
                        fg="red",
                    ),
                )
                return

        application.add_tasks(
            add,
            description,
            priority,
            today,
            week,
            deadline,
            inprogress,
            completed,
            pending,
            label,
            parent,
        )


@cli.command()
@click.pass_context
@click.option(
    "-d",
    "--desc",
    help="View and edit description of the task",
    is_flag=True,
)
@click.option(
    "-i",
    "--inprogress",
    is_flag=True,
    help="Mark Task As In Progress",
)
@click.option(
    "-c",
    "--completed",
    is_flag=True,
    help="Mark Task As Completed",
)
@click.option(
    "-pd",
    "--pending",
    is_flag=True,
    help="Mark Task As Pending",
)
@click.option(
    "-st",
    "--subtasks",
    is_flag=True,
    help="List All Subtask Of Task",
)
@click.option(
    "-w",
    "--week",
    is_flag=True,
    help="Change deadline to this week",
)
@click.option("-t", "--today", is_flag=True, help="Change deadline to today")
@click.option("-dl", "--delete", is_flag=True, help="Delete task")
@click.option("-n", "--name", help="Change the name of the task", type=str)
@click.option("-p", "--priority", help="Change the priority of the task", type=int)
@click.option("-dd", "--deadline", help="Change the deadline of the task", type=str)
@click.option("-lb", "--label", help="Change the label of the task", type=str)
@click.option("-ar", "--archive", is_flag=True, help="Edit Completed the task")
def task(
    ctx,
    desc=None,
    inprogress=None,
    completed=None,
    pending=None,
    subtasks=None,
    week=False,
    today=False,
    delete=None,
    name=None,
    priority=None,
    deadline=None,
    label=None,
    archive=False,
):
    """
    Modify a specific task.
    """

    current_task = fuzzy_search_task(archive)
    if current_task is None:
        click.echo(
            click.style(
                "Error: Task does not exist.",
                fg="red",
            ),
        )
        return

    if inprogress:
        current_task["status"] = "In Progress"
    elif pending:
        current_task["status"] = "Pending"
    elif completed:
        current_task["status"] = "Completed"

    if name:
        current_task["title"] = name
    if priority:
        current_task["priority"] = priority
    if label:
        current_task["label"] = label
    if week:
        current_task["deadline"] = "week"
    elif today:
        current_task["deadline"] = "today"
    elif deadline:
        try:
            convert_to_db_date(deadline)
            current_task["deadline"] = deadline
        except ValueError:
            click.echo(
                click.style(
                    'Error: Invalid date format, please use "dd/mm/yyyy".',
                    fg="red",
                ),
            )
            return

    if subtasks:
        tasks = application.get_subtasks_recursive(current_task)
        if tasks:
            print_tasks(
                tasks=tasks,
                plain=ctx.obj["config"]["unicode"] is False,
                subtasks=subtasks,
                pretty_tree=ctx.obj["config"]["pretty_tree"],
            )
            return

    elif desc:
        description = "No given description"
        if current_task["description"]:
            description = current_task["description"]
        current_task["description"] = click.edit(description)

    application.update_task(current_task)

    if delete:
        application.handle_delete(current_task)
        return


@cli.command()
@click.pass_context
@click.option("-l", "--list", is_flag=True, help="List all the tables")
@click.option("-a", "--add", help="Add a new table", type=str)
@click.option("-sl", "--select", help="Select a table", type=str)
@click.option("-dl", "--delete", help="Delete a table", type=str)
@click.option("-n", "--name", help="Change the name of the table", type=str)
def tables(ctx, list=None, add=None, select=None, delete=None, name=None):
    """
    Use multiple tables for segregating your tasks.
    """
    if list:
        table_list = application.list_tables()
        print_tables(table_list, ctx.obj["config"]["current_table"])
    elif add:
        table_list = application.list_tables()
        if add in table_list:
            click.echo(
                click.style(
                    "Error: Table already exists.",
                    fg="red",
                ),
            )
            return
        add, ok = sanitize_table_name(add)
        if not ok:
            click.echo(
                click.style(
                    "Error: Table name is not valid, please use only alphanumeric characters or underscores."
                    + "Maybe you are not a developer?",
                    fg="red",
                ),
            )
        ok = application.add_table(add)
        if ok:
            click.echo(
                click.style(
                    "Success: ",
                    fg="green",
                )
                + "Table stored as: "
                + click.style(add, fg="yellow"),
            )


@cli.command()
@click.pass_context
@click.option(
    "--sync",
    is_flag=True,
    help="Sync with your tasks on Jira",
)
@click.option(
    "--token",
    is_flag=True,
    help="Set private API token",
)
@click.option(
    "--url",
    is_flag=True,
    help="Set organization Jira url",
)
@click.option(
    "--email",
    is_flag=True,
    help="Set oraganization email",
)
def jira(ctx, sync=False, token=False, url=False, email=False):
    """
    Import your work from Jira
    """
    set_jira_config(ctx.obj["config"])

    if token:
        set_token()

    if url:
        set_organization_url(ctx.obj["config"])

    if email:
        set_organization_email(ctx.obj["config"])

    if sync:
        update_issues(
            ctx.obj["config"]["jira"]["url"],
            ctx.obj["config"]["jira"]["email"],
        )
        click.echo("Issues synced")


@cli.command()
@click.pass_context
def legend(ctx):
    """
    Show the legend for all special characters
    """
    if ctx.obj["config"]["unicode"]:
        print_legend()
    else:
        click.echo(
            click.style(
                "Info: Unicode is disabled, legend not required",
                fg="yellow",
            ),
        )


@cli.command()
@click.pass_context
@click.option("--migrate", is_flag=True, help="Migrate database")
@click.option(
    "--pretty_tree",
    help="Set to True for Pretty_Tree or False for rich tree",
    type=bool,
)
def init(ctx, migrate=False, pretty_tree=None):
    """
    Run after every install
    """
    if migrate:
        update_version(ctx.obj["config"])
    if pretty_tree is not None:
        ctx.obj["config"]["pretty_tree"] = pretty_tree
        update_config(config_path, ctx.obj["config"])
        click.echo(
            click.style(
                "Info: Pretty Tree setting updated",
                fg="yellow",
            ),
        )
