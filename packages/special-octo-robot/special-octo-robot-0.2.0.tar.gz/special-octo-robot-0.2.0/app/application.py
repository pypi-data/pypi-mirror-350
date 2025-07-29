import datetime

from . import database
from app.utility import convert_to_console_date
from app.utility import convert_to_db_date
from app.utility import generate_migration_error
from app.utility import sanitize_text


def list_tasks(
    table="tasks",
    priority=None,
    today=None,
    week=None,
    inprogress=None,
    completed=None,
    pending=None,
    label=None,
    subtasks=False,
) -> list | None:
    """
    List all the tasks based on the filters.
    """
    order_by = "completed ASC, status ASC, priority DESC"
    where_clause = []
    if not subtasks:
        where_clause.append("parent_id ISNULL")
    if week:
        where_clause.append(
            "(completed > date('now', 'weekday 0', '-7 days') AND completed < date('now', 'weekday 1'))",
        )
    elif today:
        where_clause.append("(completed = date('now'))")
    if inprogress or completed or pending:
        clause = []
        if inprogress:
            clause.append("'In Progress'")
        if completed:
            clause.append("'Completed'")
        if pending:
            clause.append("'Pending'")
        where_clause.append("status in (" + ",".join(clause) + ")")
    else:
        clause = ["'In Progress'", "'Pending'"]
        where_clause.append("status in (" + ",".join(clause) + ")")

    if priority:
        where_clause.append(f"priority = {priority}")

    if label:
        where_clause.append(f"label = '{label}'")
    where_clause = "WHERE " + " AND ".join(where_clause)

    try:
        results = database.list_table(
            table=table,
            columns=[
                "id",
                "title",
                "parent_id",
                "status",
                "deadline",
                "priority",
                "label",
                "description",
                "subtasks",
            ],
            where_clause=where_clause,
            order_by=f"ORDER BY {order_by}",
        )
    except Exception as e:
        print(e)
        return None

    final_results = []
    for result in results:
        final_results.append(
            {
                "id": result[0],
                "title": result[1],
                "parent_id": result[2],
                "status": result[3],
                "deadline": (
                    result[4]
                    if str(result[4]) == "None"
                    else convert_to_console_date(result[4])
                ),
                "priority": result[5],
                "label": result[6] if result[6] else "None",
                "description": result[7],
                "subtasks": result[8],
            },
        )
    return final_results


def add_tasks(
    title: str,
    table="tasks",
    description=None,
    priority=None,
    today=False,
    week=False,
    deadline=None,
    inprogress=None,
    completed=None,
    pending=None,
    label=None,
    parent=None,
):
    """
    Add a task to the database.
    """
    columns = ["title"]
    values = [f"'{sanitize_text(title)}'"]
    if description:
        columns.append("description")
        values.append(f"'{sanitize_text(description)}'")
    if priority:
        columns.append("priority")
        values.append(str(priority))
    if today:
        columns.append("deadline")
        values.append("date('now')")
    elif week:
        columns.append("deadline")
        values.append("date('now', 'weekday 0')")
    elif deadline:
        columns.append("deadline")
        values.append(f"'{deadline}'")
    if inprogress:
        columns.append("status")
        values.append("'In Progress'")
    elif completed:
        columns.append("status")
        values.append("'Completed'")
    elif pending:
        columns.append("status")
        values.append("'Pending'")
    if label:
        columns.append("label")
        values.append(f"'{sanitize_text(label)}'")
    if parent:
        columns.append("parent_id")
        values.append(str(parent["id"]))
    try:
        database.insert_into_table(table, columns=columns, values=values)
    except Exception as e:
        print(e)
        return
    # Insert the record then increment the count of the parent task.
    if parent:
        database.update_table(
            table,
            {"subtasks": "subtasks + 1", "id": f"{parent['id']}"},
        )


def search_task(task_id, table: str) -> dict | None:
    """
    Search a task by its id.
    :param task_id:
    :return: task_details
    """
    try:
        task = database.list_table(
            table=table,
            columns=[
                "id",
                "title",
                "description",
                "status",
                "deadline",
                "priority",
                "label",
                "completed",
                "parent_id",
                "subtasks",
            ],
            where_clause=f"WHERE id = {task_id}",
        )
    except:
        generate_migration_error()
        return None

    task_details = {}
    if task:
        task = task[0]
        task_details = {
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "status": task[3],
            "deadline": task[4],
            "priority": task[5],
            "label": task[6] if task[6] else "None",
            "completed": (task[7]),
            "parent_id": task[8],
            "subtasks": task[9],
        }
    return task_details


def get_subtasks(task_id: int, table: str):
    try:
        results = database.list_table(
            table=table,
            columns=[
                "id",
                "title",
                "status",
                "deadline",
                "priority",
                "label",
                "description",
                "subtasks",
                "parent_id",
            ],
            where_clause=f"WHERE parent_id = {task_id}",
            order_by="ORDER BY completed ASC, status ASC, priority DESC",
        )
    except:
        generate_migration_error()
        return None
    final_results = []
    for result in results:
        final_results.append(
            {
                "id": result[0],
                "title": result[1],
                "status": result[2],
                "deadline": (
                    result[3]
                    if str(result[3]) == "None"
                    else convert_to_console_date(result[3])
                ),
                "priority": result[4],
                "label": result[5] if result[5] else "None",
                "description": result[6],
                "subtasks": result[7],
                "parent_id": result[8],
            },
        )
    return final_results


def get_subtasks_recursive(task: dict, table: str):
    if task["subtasks"] == 0:
        return []

    final_results = [task]
    for child in get_subtasks(task["id"], table):
        final_results.append(child)
        final_results.extend(get_subtasks_recursive(child), table)
    return final_results


def update_task(updated_data: dict, table: str):
    """If marked as completed then set datetime as now else retain prev value"""

    if updated_data["deadline"] == "week":
        today = datetime.date.today()
        weekend = today + datetime.timedelta(days=6 - today.weekday())
        updated_data["deadline"] = str(weekend)
    elif updated_data["deadline"] == "today":
        updated_data["deadline"] = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    elif updated_data["deadline"] not in [None, "None"]:
        updated_data["deadline"] = str(convert_to_db_date(updated_data["deadline"]))

    if updated_data["status"] == "Completed":
        updated_data["completed"] = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    else:
        updated_data["completed"] = updated_data["deadline"]

    final_data = {}

    for key, value in updated_data.items():
        if value is None:
            continue

        if type(value) is str:
            updated_data[key] = f"'{sanitize_text(value)}'"

        final_data[key] = updated_data[key]

    try:
        database.update_table(table, final_data)
    except Exception as e:
        print(e)
        generate_migration_error()
        return
    if updated_data["subtasks"] != 0 and updated_data["status"] == "'Completed'":
        children = get_subtasks(updated_data["id"], table)
        for child in children:
            child["status"] = "Completed"
            try:
                update_task(child, table)
            except Exception:
                generate_migration_error()


def handle_delete(current_task: dict, table: str):
    """
    Delete a task from the database
    """
    database.delete_task(table, current_task["id"])
    children = database.list_table(
        table=table,
        columns=["id", "parent_id"],
        where_clause=f"WHERE parent_id = {current_task['id']}",
    )
    for child in children:
        handle_delete({"id": child[0], "parent_id": child[1]}, table)
    if current_task["parent_id"]:
        parent = search_task(current_task["parent_id"], table)
        if parent and parent["subtasks"] > 0:
            try:
                database.update_table(
                    "tasks",
                    {"subtasks": "subtasks - 1", "id": f"{current_task['parent_id']}"},
                )
            except:
                generate_migration_error()


def list_tables() -> list:
    """
    List all the tables in the database.
    """
    try:
        res = database.list_tables()
    except:
        generate_migration_error()
        return []

    result = []
    for table in res:
        if table[0] != "sqlite_sequence":
            result.append(table[0])
    return result


def add_table(table_name: str) -> bool:
    """
    Add a table to the database.
    """
    try:
        database.initialize(table_name)
        return True
    except Exception as e:
        print(e)
        return False


def delete_table(table_name: str) -> bool:
    """
    Delete a table from the database.
    """
    try:
        database.delete_table(table_name)
        return True

    except Exception as e:
        print(e)
        return False


def rename_table(old_name: str, new_name: str) -> bool:
    """
    Rename a table in the database.
    """
    try:
        database.rename_table(old_name, new_name)
        return True
    except Exception as e:
        print(e)
        return False
