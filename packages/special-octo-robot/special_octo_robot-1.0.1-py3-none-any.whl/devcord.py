import os

import click

from app import application
from app.config import check_unicode_support
from app.config import get_config
from app.config import initialize_config
from app.config import update_config
from app.console import print_legend
from app.console import print_session_data
from app.console import print_sessions
from app.console import print_tables
from app.console import print_tasks
from app.constants import config_path
from app.constants import db_path
from app.constants import path
from app.database import initialize
from app.helper import check_table_exists
from app.helper import lister
from app.helper import session_lister
from app.migrations import update_version
from app.utility import check_if_relative_deadline
from app.utility import convert_time_to_epoch
from app.utility import display_error_message
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
        display_error_message(
            "Could not find the path to the database, raise an issue with the developers.",
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
    "-dt",
    "--date",
    help='Perform for all the tasks for this date, example date format: "dd/mm/yyyy/"',
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
@click.option("--path", help="Specify Output File", type=click.Path(exists=True))
@click.option("-st", "--subtask", is_flag=True, help="List or add subtasks")
@click.option("-tb", "--table", help="Specify Table", type=str)
def tasks(
    ctx,
    list=None,
    add=None,
    desc=None,
    priority=None,
    today=False,
    week=False,
    date=None,
    inprogress=None,
    completed=None,
    pending=None,
    label=None,
    output=None,
    path=None,
    subtask=False,
    table=None,
):
    """
    Create and List tasks.
    """

    if not table:
        table = ctx.obj["config"].get("current_table", "tasks")

    if not add and not list:
        display_error_message("Please specify an action.")
        return

    if date:
        date = check_if_relative_deadline(date)
        if date is False:
            return

        err = convert_time_to_epoch(date)
        if type(err) == str:
            display_error_message(date)
            click.echo('Example: "01/01/2020"')
            return

    if list:

        task_list = application.list_tasks(
            table=table,
            priority=priority,
            today=today,
            week=week,
            inprogress=inprogress,
            completed=completed,
            pending=pending,
            label=label,
            subtasks=subtask,
            date=date,
        )

        if (
            priority is not None
            or today
            or week
            or inprogress
            or completed
            or pending
            or label
        ):
            subtask = False

        if task_list:
            print_tasks(
                task_list,
                output,
                path,
                ctx.obj["config"]["unicode"] is False,
                subtask,
                table,
                pretty_tree=ctx.obj["config"].get("pretty_tree", True),
            )
        else:
            click.echo(
                click.style(
                    "Info: No tasks found.",
                    fg="yellow",
                ),
            )

    elif add:
        parent = None
        description = "No given description"
        if desc:
            description = click.edit()
        if subtask:
            parent = lister(
                table=table,
            )

            if parent is None:
                display_error_message("Parent task does not exist.")
                return

            children = [
                item["title"] for item in application.get_subtasks(parent["id"], table)
            ]
        else:
            children = [item["title"] for item in application.list_tasks(table=table)]

        if add in children:
            display_error_message("Task with same name already exists on this level.")
            return

        application.add_tasks(
            add,
            table,
            description,
            priority,
            today,
            week,
            date,
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
@click.option("-tb", "--table", help="Specify Table", type=str)
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
    table=None,
):
    """
    Modify a specific task.
    """

    if table is None:
        table = ctx.obj["config"].get("current_table", "tasks")

    current_task = lister(
        table=table,
        completed=archive,
    )

    if current_task is None:
        display_error_message("Task does not exist.")
        return

    update_config(config_path, ctx.obj["config"])

    if inprogress:
        current_task["status"] = "In Progress"
    elif pending:
        current_task["status"] = "Pending"
    elif completed:
        current_task["status"] = "Completed"

    if name:
        current_task["title"] = name
        parent_id = current_task.get("parent_id", -1)
        if parent_id:
            children = [
                item["title"] for item in application.get_subtasks(parent_id, table)
            ]
        else:
            children = [item["title"] for item in application.list_tasks(table=table)]
        if name in children:
            display_error_message("Task with same name already exists on this level.")
            return

    if priority:
        current_task["priority"] = priority
    if label:
        current_task["label"] = label
    if week:
        current_task["deadline"] = "week"
    elif today:
        current_task["deadline"] = "today"
    elif deadline:

        deadline = check_if_relative_deadline(deadline)
        if deadline is False:
            return

        err = convert_time_to_epoch(deadline)
        if type(err) == str:
            display_error_message(err)
            click.echo('Example: "01/01/2020"')
            return
        current_task["deadline"] = deadline

    if subtasks:
        task_list = application.get_subtasks_recursive(current_task, table)
        if task_list:
            temp = current_task.copy()
            temp["parent_id"] = -1
            # For subtasks, the parent of the parent node is irrelevant
            # Parent_id cannot be -1, therefore functions ahead can recognize this node as root.
            task_list.append(temp)
            print_tasks(
                tasks=task_list,
                plain=ctx.obj["config"]["unicode"] is False,
                subtasks=subtasks,
                table_name=table,
                pretty_tree=ctx.obj["config"].get("pretty_tree", True),
            )
            return

    elif desc:
        description = "No given description"
        if current_task["description"]:
            description = current_task["description"]
        current_task["description"] = click.edit(description)

    application.update_task(current_task, table)

    if delete:
        application.handle_delete(current_task, table=table)
        update_config(config_path, ctx.obj["config"])
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
        print_tables(table_list, ctx.obj["config"].get("current_table", "tasks"))

    elif add:
        exists, add = check_table_exists(add)
        if exists:
            display_error_message("Table already exists.")
            return

        ok = application.add_table(add)

        if ok:
            click.echo(
                click.style(
                    "Success: ",
                    fg="green",
                )
                + "Table stored as "
                + add,
            )

    elif select:
        exists, select = check_table_exists(select)
        if not exists:
            display_error_message("Table does not exist.")
            return

        ctx.obj["config"]["current_table"] = select
        update_config(config_path, ctx.obj["config"])

        click.echo(
            click.style(
                "Success: ",
                fg="green",
            )
            + "Table selected "
            + select,
        )

    elif delete:
        exists, delete = check_table_exists(delete)
        if not exists:
            display_error_message("Table does not exist.")
            return
        if application.list_tables() == 1:
            display_error_message("Cannot delete the only table.")
            return

        if ctx.obj["config"].get("current_table", "tasks") == delete:
            display_error_message("Cannot delete curently selected table.")
            return
        ok = application.delete_table(delete)

        if ok:
            click.echo(
                click.style(
                    "Success: ",
                    fg="green",
                )
                + "Table deleted: "
                + delete,
            )

    elif name:
        exists, name = check_table_exists(name)
        if not exists:
            display_error_message("Table does not exist.")
            return

        new_name = click.prompt(
            "Enter new name for the table",
            default=name,
            show_default=False,
        )

        ok = application.rename_table(name, new_name)

        if ok:
            if name == ctx.obj["config"]["current_table"]:
                ctx.obj.config["current_table"] = new_name
                update_config(config_path, ctx.obj.config)
            click.echo(
                click.style(
                    "Success: ",
                    fg="green",
                )
                + "Table renamed from "
                + click.style(name, fg="yellow")
                + " to: "
                + click.style(new_name, fg="yellow"),
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
        exists, _ = check_table_exists("jira")
        if not exists:
            application.add_table("jira")

        update_issues(
            ctx.obj["config"]["jira"]["url"],
            ctx.obj["config"]["jira"]["email"],
            "jira",
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
@click.option("--pretty_tree", help="Change the name of the task", type=bool)
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


@cli.command()
@click.pass_context
@click.option("-st", "--start", is_flag=True, help="Start a session for a task")
@click.option("-ed", "--end", is_flag=True, help="End the current session")
@click.option("-l", "--list", is_flag=True, help="List all the sessions")
@click.option("-sl", "--select", is_flag=True, help="Select a session to view")
@click.option("-fl", "--filter", is_flag=True, help="Filter sessions by task")
@click.option("-dl", "--delete", is_flag=True, help="Delete a session")
def session(ctx, start, end, list, select, filter, delete):
    """
    Manage sessions for tasks.
    """
    table = ctx.obj["config"].get("current_table", "tasks")
    current_task = None
    if filter:
        current_task = lister(table=table)
        if current_task is None:
            display_error_message("No tasks available to start a session.")
            return

    if start:
        if not current_task:
            current_task = lister(table=table)
        if current_task is None:
            display_error_message("No tasks available to start a session.")
            return

        session_data = ctx.obj["config"].get("session_data", {})
        session_data = application.start_session(
            current_task["id"],
            table,
            session_data,
        )
        if session_data is not None:
            ctx.obj["config"]["session_data"] = session_data
            update_config(config_path, config=ctx.obj["config"])
            click.echo(
                click.style(
                    f"Session started for task: {current_task['title']}",
                    fg="green",
                ),
            )
            os._exit(0)
        else:
            display_error_message("Could not start session.")

        # code to handle else
    elif end:
        session_data = ctx.obj["config"].get("session_data", {})
        session_data = application.end_session(session_data)
        ctx.obj["config"]["session_data"] = session_data

    elif list:
        sessions = application.list_sessions(
            table=table,
            task_id=current_task["id"] if filter else None,
        )
        if sessions:
            print_sessions(sessions)
        else:
            click.echo(
                click.style(
                    "Info: No sessions found.",
                    fg="yellow",
                ),
            )
    elif select:
        session = session_lister(
            table=table,
            task_id=current_task["id"] if filter else None,
        )
        if session is None:
            display_error_message("No session exists.")
            return

        session_data = application.get_session_data(session_id=session["id"])
        if session_data is None:
            display_error_message("No session data exists.")
            return
        session_data["title"] = session["title"]
        print_session_data(session_data)

    elif delete:
        session = session_lister(
            table=table,
            task_id=current_task["id"] if filter else None,
        )
        if session is None:
            display_error_message("No session exists.")
            return

        application.delete_session(session_id=session["id"])
        click.echo(
            click.style(
                f"Session {session['title']} deleted successfully.",
                fg="green",
            ),
        )

    else:
        display_error_message("Please specify an action (--start or --end).")
