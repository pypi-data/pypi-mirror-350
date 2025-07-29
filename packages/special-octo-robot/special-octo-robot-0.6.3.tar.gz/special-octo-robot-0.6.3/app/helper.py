import curses

from click import echo
from click import style

from app import application
from app.console_helper import treeify
from app.constants import CR_ENTER
from app.constants import LF_ENTER
from app.utility import sanitize_table_name


def check_table_exists(table_name: str) -> bool:
    table_name, ok = sanitize_table_name(table_name)
    if not ok:
        echo(
            style(
                "Error: Table name is not valid, please use only alphanumeric characters or underscores."
                + "Maybe you are not a developer?",
                fg="red",
            ),
        )
    return table_name in application.list_tables(), table_name


def lister(table, completed=False):
    tasks = application.list_tasks(table, subtasks=True, completed=completed)

    if len(tasks) == 0:
        return None

    tree = treeify(tasks)

    def get_tasks(task_id):
        if task_id == None:
            return {}, []
        if task_id == -1:
            return {"title": table, "id": -1}, tree[-1]["children"]
        return tree[task_id]["data"], tree[task_id]["children"]

    return curses.wrapper(menu, -1, get_tasks)


def menu(stdscr, current: int, get_tasks) -> dict:
    """
    'current' is the id of the current task;
    'get_tasks' is a function that takes an id and returns the task and its subtasks.
    If id is None, it returns None, and empty list.
    If id is -1, it returns root task and its subtasks.
    """
    curses.curs_set(0)
    stdscr.keypad(1)

    selected = 0
    current_task, _ = get_tasks(current)  # get initial list of tasks
    parent, options_left = get_tasks(
        current_task.get("parent_id", None),
    )  # for one page of tasks, parent is the same so get them once before hand

    while True:
        stdscr.clear()
        current_task, options = get_tasks(current)
        title = current_task["title"]

        height, width = stdscr.getmaxyx()
        # Leave space for top/bottom margins
        height -= 2
        width -= 1

        if len(title) > 30:
            title = title[:30] + "..."

        start_y = 1
        start_x = 1
        stdscr.addstr(start_y, start_x, f"{title}:")
        if len(options_left) > 0:
            stdscr.addstr(start_y + 1, start_x + 1, "<<-- prev")

        if len(options) > 0:
            _, options_right = get_tasks(options[selected]["data"]["id"])
            if len(options_right) > 0:
                stdscr.addstr(start_y + 1, start_x + 15, "next -->>")

        delta_x = 2
        delta_y = start_y + 3

        max_page_size = height - delta_y + 1

        idx = 0
        page_size = min(max_page_size, len(options))
        if len(options) > max_page_size:
            idx = selected
            page_size = min(max_page_size, len(options) - selected) + selected
            delta_y -= selected

        while idx < page_size:
            option = options[idx]
            title = option["data"]["title"]
            if len(title) > width - 2:
                title = title[: width - 5] + "..."

            if idx == selected:
                stdscr.addstr(
                    idx + delta_y,
                    delta_x,
                    title,
                    curses.A_REVERSE,
                )
            else:
                stdscr.addstr(idx + delta_y, delta_x, title)
            idx += 1

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)

        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)

        elif key == curses.KEY_RIGHT and len(options_right) > 0:
            current = options[selected]["data"]["id"]
            options_left = options
            parent = current_task
            options = options_right
            selected = 0

        elif key == curses.KEY_LEFT and len(options_left) > 0:
            options = options_left
            for idx, option in enumerate(options):
                if option["data"]["id"] == current:
                    selected = idx
                    break
            current = parent["id"]
            parent, options_left = get_tasks(current_task.get("parent_id", None))

        elif key in [curses.KEY_ENTER, LF_ENTER, CR_ENTER] and len(options) > 0:
            return options[selected]["data"]
