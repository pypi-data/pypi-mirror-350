import app.database as db
from app.utility import generate_migration_error


def search_task(title):
    """
    Search a task by it's title.
    """
    try:
        task = db.list_table(
            table="tasks",
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
            where_clause=f"WHERE title = '{title}'",
        )
    except:
        generate_migration_error()
        return {}
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
