import app.database as db


def search_task(key):
    """
    Search a task by it's title.
    """
    try:
        task = db.list_table(
            table="jira",
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
            where_clause=f"WHERE title LIKE '{key}%'",
        )
    except Exception as e:
        print(e)
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
