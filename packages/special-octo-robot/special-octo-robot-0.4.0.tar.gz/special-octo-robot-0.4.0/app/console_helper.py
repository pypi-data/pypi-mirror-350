import os

from click import echo
from click import style


def get_priority_color(priority):
    if priority == 5:
        return "bold red"
    elif priority == 4:
        return "#EE4B2B"
    elif priority == 3:
        return "magenta"
    elif priority == 2:
        return "blue"
    elif priority == 1:
        return "cyan"
    else:
        return "#FFFFFF"


def get_status_color(status):
    if status == "Completed":
        return "#50C878"
    elif status == "Pending":
        return "bold red"
    else:
        return "#FFFFFF"


def sanitize_path(path):
    if path[-1] == "/":
        echo(
            style(
                text="Error: Path is a directory, please provide a file path.",
                fg="red",
            ),
        )
        return False
    if not os.path.exists(os.path.dirname(path)):
        echo(
            style(
                text="Error: The directory where you are trying to store the file in does not exist.",
                fg="red",
            ),
        )
        return False
    return True


def treeify(tasks, title="Tasks"):

    root = {"data": title, "children": []}
    existing_node = {}

    for task in tasks:
        if task["parent_id"] in (None, -1):
            if existing_node.get(task["id"], False):
                existing_node[task["id"]]["data"] = task
            else:
                existing_node[task["id"]] = {"data": task, "children": []}
            if task["parent_id"] == -1:
                root = existing_node[task["id"]]
            else:
                root["children"].append(existing_node[task["id"]])
        else:

            if task["id"] in existing_node:
                existing_node[task["id"]]["data"] = task
            else:
                existing_node[task["id"]] = {"data": task, "children": []}

            if task["parent_id"] not in existing_node:
                parent_task = {
                    "data": {},
                    "children": [],
                }  # temparary node for adding child
                existing_node[task["parent_id"]] = parent_task

            existing_node[task["parent_id"]]["children"].append(
                existing_node[task["id"]],
            )
    return root
