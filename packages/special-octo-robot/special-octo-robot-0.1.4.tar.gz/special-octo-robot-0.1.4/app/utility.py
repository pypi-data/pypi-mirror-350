import datetime

from click import echo
from click import style
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.completion import ThreadedCompleter

from app import application


def convert_to_console_date(date_str, title=None):
    """
    Convert date from "YYYY-MM-DD" to "dd/mm/yyyy"
    """
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d/%m/%Y")


def convert_to_db_date(date_str):
    # Convert date from "dd/mm/yyyy" to "YYYY-MM-DD"
    date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
    return date_obj.strftime("%Y-%m-%d")


def sanitize_text(text):
    return text.strip().replace("'", '"')


def fuzzy_search_task(completed=False) -> dict:
    all_tasks = application.list_tasks(subtasks=True, completed=completed)
    task_titles = [each_task["title"] for each_task in all_tasks]

    task_completer = ThreadedCompleter(FuzzyWordCompleter(task_titles))
    select_task_title = prompt(
        "Enter any part from title of the task: \n",
        completer=task_completer,
    )

    current_task = next(
        (
            each_task
            for each_task in all_tasks
            if each_task["title"] == select_task_title
        ),
        None,
    )
    return current_task


def generate_migration_error():
    echo(
        style(
            "Have You Run Migrations? Run 'devcord init --migrate' to run migrations",
            fg="red",
        ),
    )


def sanitize_table_name(table_name: str) -> (str, bool):
    for ch in table_name:
        if ch.isalnum() or ch == " " or ch == "_":
            continue
        else:
            return "", False

    return table_name.replace(" ", "_"), True
