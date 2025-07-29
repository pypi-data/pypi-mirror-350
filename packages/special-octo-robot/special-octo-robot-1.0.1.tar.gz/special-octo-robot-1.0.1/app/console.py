import json
import os

import PrettyPrint
from click import echo
from click import style
from PrettyPrint import PrettyPrintTree
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from . import console_helper


def get_table(tasks, plain=False):
    table = Table(title="Tasks", highlight=True, leading=True)
    table.add_column("Priority", justify="center", style="white")
    table.add_column("Task", justify="left", style="white")
    table.add_column("Status", justify="center", style="white")
    table.add_column("Deadline", justify="center", style="white")
    table.add_column("Label", justify="center", style="white")
    table.add_column("Properties", justify="center", style="white")
    text_style = Style(color="#FFFFFF")
    bold_text_style = Style(color="#FFFFFF", bold=True)
    none_style = Style(color="magenta")
    for task in tasks:
        properties = []
        if task["description"] and task["description"] not in [
            "None",
            "No given description",
        ]:
            if plain:
                properties.append("Description")
            else:
                properties.append("►")
        if task["subtasks"] > 0:
            if plain:
                properties.append("Subtasks")
            else:
                properties.append("|☰")

        table.add_row(
            (
                f"[{console_helper.get_priority_color(task['priority'])}]{task['priority']}"
                if not plain
                else f"[{text_style}]{task['priority']}"
            ),
            f'[{text_style}]{task["title"]}',
            f'[{console_helper.get_status_color(task["status"])}][italic]{task["status"]}',
            task["deadline"],
            f'[{bold_text_style if task["label"] != "None" else none_style}]{task["label"]}',
            f"[{text_style}]{','.join(properties)}",
        )
    return table


def print_tree(tasks, table_name="Tasks", pretty_tree=True):

    # TODO use the moved out the logic of forming the tree and have to only print it here
    def parse_subtask_string(task):
        if pretty_tree == False:
            text = Text()
            text.append(f" {task['title']}\n", style="italic bold")
            text.append("Priority: ", style="dim")
            text.append(
                f"{task['priority']} ",
                style=f"{console_helper.get_priority_color(task['priority'])}",
            )
            text.append(f"| {task['deadline']} | ", style="dim")
            text.append(
                f"{task['status']} ",
                style=console_helper.get_status_color(task["status"]) + " dim",
            )
            text.append(f"| {task['label']}\n", style="dim")
            # return f" [italic]{task['title']}\n[bold]Priority: [white]{task['priority']} | {task['deadline']}| {task['status']} | {task['label']}\n"
            return text
        else:
            return f"{task['title']}\nPriority: | {task['deadline']}| {task['status']} | {task['label']}"

    root = Tree("\n" + table_name + "\n", style="bold")
    root.guide_style = "bold blue"
    existing_node = {}

    for task in tasks:

        if task["parent_id"] in (None, -1):
            if existing_node.get(task["id"], False):
                existing_node[task["id"]].label = parse_subtask_string(task)
            else:
                existing_node[task["id"]] = Tree(parse_subtask_string(task))
            if task["parent_id"] == -1:
                root = existing_node[task["id"]]
            else:
                existing_node[task["id"]].guide_style = "yellow"
                root.children.append(existing_node[task["id"]])
        else:

            if task["id"] in existing_node:
                existing_node[task["id"]].label = parse_subtask_string(task)
            else:
                existing_node[task["id"]] = Tree(parse_subtask_string(task))

            if task["parent_id"] not in existing_node:
                parent_task = Tree("temp")  # temparary node for adding child
                existing_node[task["parent_id"]] = parent_task

            existing_node[task["id"]].guide_style = "yellow"
            existing_node[task["parent_id"]].children.append(existing_node[task["id"]])

    if pretty_tree:
        pt = PrettyPrintTree(
            lambda x: x.children,
            lambda x: x.label,
            border=False,
            orientation=PrettyPrintTree.Horizontal,
        )
        pt(root)
    else:
        return root


def print_tasks(
    tasks,
    output=None,
    path=None,
    plain=False,
    subtasks=False,
    table_name="Tasks",
    pretty_tree=True,
):
    if subtasks:
        if output == "json":
            result = console_helper.treeify(tasks)[-1]
        elif output or path or pretty_tree == False:
            # passing result ahead as rich can print its own object
            result = print_tree(tasks, table_name, False)
        else:
            print_tree(tasks, table_name)
            return

    # Setting where the output will be sent
    file = None
    if path:
        path = path.strip()
        if path[0] != "/":  # If path is not absolute
            path = os.path.join(os.getcwd(), path)

        if not console_helper.sanitize_path(path):
            return

        file = open(path, "w+")
        console = Console(file=file)
    else:
        console = Console()

    # Handling output format
    if path:
        plain = True
    if output == "json":
        if subtasks:
            result = json.dumps(tasks, indent=4)
        console.print_json(result)

    elif output == "text":
        if subtasks:
            console.print(result)
        else:
            console.print(f"[bold]{table_name}")
            console.rule()
            index = 1
            for task in tasks:
                console.print(
                    f"{index}) Title: {task['title']}\n- Description: {task['description']}\n- Deadline: {task['deadline']}\n",
                )
                index += 1

    else:
        if not subtasks:
            result = get_table(tasks, plain)
        console.print(result)

    if file:
        file.close()


def print_legend():
    text_style = Style(color="#FFFFFF")
    console = Console()
    table = Table(title="Priority Legend", highlight=True, leading=True)
    table.add_column("Unicode Character", justify="center", style="white")
    table.add_column("Value", justify="center", style="white")
    table.add_row(
        f"[{console_helper.get_priority_color(0)}]●",
        f"[{text_style}]No Priority Level",
    )
    for i in range(1, 6):
        table.add_row(
            f"[{console_helper.get_priority_color(i)}]●",
            f"[{text_style}]Priority level: {i}",
        )
    console.print(table)
    console.rule()
    table = Table(title="Task Properties Legend", highlight=True, leading=True)
    table.add_column("Unicode Character", justify="center", style="white")
    table.add_column("Value", justify="center", style="white")
    table.add_row("[#FFFFFF]►", f"[{text_style}]Has description")
    table.add_row("[#FFFFFF]|☰", f"[{text_style}]Has subtasks")
    console.print(table)


def print_tables(tables, current_table):
    console = Console()
    table = Table(title="Task Lists", highlight=True, leading=True)
    table.add_column("List Name", justify="center", style="white")
    for table_name in tables:
        if table_name == current_table:
            table.add_row(f"[#FFFFFF][italic]-> {table_name}")
        else:
            table.add_row(f"[#FFFFFF]{table_name}")
    console.print(table)


def print_sessions(sessions):
    console = Console()
    table = Table(title="Session", highlight=True, leading=True)
    table.add_column("Task", justify="left", style="white")
    table.add_column("Start Time", justify="left", style="white")
    table.add_column("End Time", justify="left", style="white")
    table.add_column("Duration", justify="left", style="white")
    for session in sessions:
        table.add_row(
            f"[#FFFFFF]{session['task_name']}",
            f"[#FFFFFF]{session['start_datetime']}",
            f"[#FFFFFF]{session['end_datetime']}",
            f"[#FFFFFF]{session['duration']}",
        )
    console.print(table)


def print_session_data(session_data):
    console = Console()
    table = Table(title=session_data["title"], highlight=True, leading=True)
    table.add_column("Application Name", justify="left", style="white")
    table.add_column("Duration", justify="left", style="white")
    for session in session_data["data"]:
        table.add_row(
            f"[#FFFFFF]{session['application_name']}",
            f"[#FFFFFF]{session['duration']}",
        )
    console.print(table)
