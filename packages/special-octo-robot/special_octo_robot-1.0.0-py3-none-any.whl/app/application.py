import datetime
import json
import time

from . import database
from app.sessions.linux import session_end as linux_session_end
from app.sessions.linux import session_start as linux_session_start
from app.utility import convert_epoch_to_date
from app.utility import convert_epoch_to_datetime
from app.utility import convert_seconds_delta_to_time
from app.utility import convert_time_to_epoch
from app.utility import display_error_message
from app.utility import display_info_message
from app.utility import generate_migration_error
from app.utility import get_os
from app.utility import get_week_start
from app.utility import get_weekend
from app.utility import sanitize_text


def list_tasks(
    table="tasks",
    priority=None,
    today=None,
    week=None,
    date=None,
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
        mond = convert_time_to_epoch(get_week_start(), False)
        sund = convert_time_to_epoch(get_weekend())
        where_clause.append(
            f"(completed >= {mond} AND completed <= {sund})",
        )
    elif today:
        today = get_deadline("today")
        where_clause.append(
            f"(completed >= {convert_time_to_epoch(today, False)} AND completed <= {convert_time_to_epoch(today)})",
        )
    elif date:
        where_clause.append(
            f"(completed >= {convert_time_to_epoch(date, False)} AND completed <= {convert_time_to_epoch(date)})",
        )
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
                "deadline": (convert_epoch_to_date(result[4])),
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
        values.append(f"{convert_time_to_epoch(get_deadline('today'))}")
    elif week:
        columns.append("deadline")
        values.append(f"{convert_time_to_epoch(get_deadline('week'))}")
    elif deadline:
        columns.append("deadline")
        values.append(f"{convert_time_to_epoch(deadline)}")
    if inprogress:
        columns.append("status")
        values.append("'In Progress'")
    elif completed:
        columns.append("status")
        values.append("'Completed'")
        columns.append("completed")
        values.append(f"{convert_time_to_epoch(get_deadline('today'))}")
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
            "deadline": convert_epoch_to_date(task[4]),
            "priority": task[5],
            "label": task[6] if task[6] else "None",
            "completed": convert_epoch_to_date(task[7]),
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
                "deadline": (convert_epoch_to_date(result[3])),
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

    updated_data["deadline"] = get_deadline(updated_data["deadline"])

    if updated_data["status"] == "Completed":
        updated_data["completed"] = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    else:
        updated_data["completed"] = updated_data["deadline"]

    updated_data["deadline"] = convert_time_to_epoch(updated_data["deadline"])
    updated_data["completed"] = convert_time_to_epoch(updated_data["completed"])

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
                    table,
                    {"subtasks": "subtasks - 1", "id": f"{current_task['parent_id']}"},
                )
            except Exception as e:
                print(e)


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
        if table[0] not in ("sqlite_sequence", "sessions", "session_data"):
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


def get_deadline(deadline):
    if deadline == "week":
        deadline = str(get_weekend())
    elif deadline == "today":
        deadline = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    else:
        deadline = str(deadline)

    return deadline


def start_session(task_id: int, table: str, session_data: dict):
    """
    Start a session for a task.
    """
    # TODO: Write database calls
    if session_data.get("pid", 0) > 0:
        # If a session is already active, end it first
        end_session(session_data)
        display_info_message("A session was already active, ending it.")

    if get_os() == "Linux":
        try:
            pid, filehandle = linux_session_start()
            session_data["pid"] = pid
            session_data["file_handle"] = filehandle
        except Exception as e:
            display_error_message(f"Failed to start session: {e}")
            return None

    # Start a new session
    session_data["start_time"] = int(datetime.datetime.now().timestamp())
    session_data["task_id"] = task_id
    session_data["table"] = table
    display_info_message("Session started.")
    return session_data


def end_session(session_data: dict):
    """
    End the current session.
    """
    if session_data.get("pid", 0) == 0:
        return

    data = {}

    if get_os() == "Linux":
        try:
            ok, err = linux_session_end(session_data["pid"])
            if not ok:
                if err is not None:
                    display_error_message(f"Failed to end session: {err}")
                return None
            with open(session_data["file_handle"], "r") as f:
                time.sleep(1)
                content = f.read().strip()
                if not content:
                    display_error_message("Session file is empty.")
                    return None
                data = json.loads(content)

        except Exception as e:
            display_error_message(f"Failed to end session: {e}")
            return None

    session_data["end_time"] = int(datetime.datetime.now().timestamp())

    session_id = database.add_session(
        task_id=session_data["task_id"],
        table_name=session_data["table"],
        start_datetime=session_data["start_time"],
        end_datetime=session_data["end_time"],
    )
    session_data["session_id"] = session_id
    mapped_data = {}
    for value in data.values():
        if value["name_list"]:
            name = "-".join(value["name_list"])
            if mapped_data.get(name, None) is None:
                mapped_data[name] = value["time"]
            else:
                mapped_data[name] += value["time"]
    for key, value in mapped_data.items():
        database.add_session_data(
            session_id=session_id,
            application_name=key,
            duration=value,
        )

    return {"session_id": session_id, "session_data": session_data}


def list_sessions(table: str, task_id: int = None) -> list:
    """
    List all the sessions, filter by task_id.
    """
    try:
        sessions = database.list_sessions(table, task_id)
    except Exception as e:
        print(e)
        return []

    session_list = []

    for session in sessions:
        task = search_task(session[1], table)
        duration = session[4] - session[3]
        if duration < 0:
            duration = 0

        session_list.append(
            {
                "session_id": session[0],
                "task_name": task["title"],
                "start_datetime": convert_epoch_to_datetime(session[3]),
                "end_datetime": convert_epoch_to_datetime(session[4]),
                "duration": convert_seconds_delta_to_time(duration),
            },
        )

    return session_list


def get_session_data(session_id: int) -> dict:
    """
    Get session data for a given session ID.
    """
    try:
        session_data = database.get_session_data(session_id)
        data = {
            "data": [],
        }
        for session_item in session_data:
            data["data"].append(
                {
                    "application_name": session_item[2],
                    "duration": convert_seconds_delta_to_time(session_item[3]),
                },
            )
        return data
    except Exception as e:
        print(e)
        return {}


def delete_session(session_id: int) -> bool:
    """
    Delete a session by its ID.
    """
    try:
        database.delete_session(session_id)
        return True
    except Exception as e:
        display_error_message(f"Failed to delete session: {e}")
        return False
