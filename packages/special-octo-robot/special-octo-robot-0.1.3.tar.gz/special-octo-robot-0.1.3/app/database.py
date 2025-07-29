import sqlite3

from app.constants import db_path


def initialize():
    """
    Initialize the database with all the necessary tables.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL, parent_id INTEGER,
        description TEXT DEFAULT 'None',
        status VARCHAR DEFAULT 'Pending',
        deadline DATE DEFAULT 'None',
        priority INTEGER DEFAULT 0,
        label VARCHAR DEFAULT 'None',
        completed DATE,
        subtasks INTEGER DEFAULT 0
        )""",
    )
    cur.execute(
        """
        CREATE TRIGGER initialize_completed_column
        AFTER INSERT ON tasks
        FOR EACH ROW
        BEGIN
            UPDATE tasks SET completed = NEW.deadline WHERE id = NEW.id;
        END;
    """,
    )


def list_table(
    table: str,
    columns: list,
    where_clause: str = "",
    group_clause: str = "",
    order_by: str = "",
) -> list:
    """
    List data from a table.
    """
    query = f"SELECT {', '.join(columns)} FROM {table} {where_clause} {group_clause} {order_by}"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    res = cur.execute(query).fetchall()
    return res


def insert_into_table(table: str, columns: list, values: list) -> None:
    """
    Insert data into a table.
    """
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)})"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()


def update_table(table: str, new_data: dict) -> None:
    """
    Update Values Of Given Table
    """
    set_clause = ", ".join(
        [f"{key} = {value}" for key, value in new_data.items() if key != "id"],
    )
    query = f"UPDATE {table} SET {set_clause} WHERE id = {new_data['id']}"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()


def delete_task(task_id: int) -> None:
    """
    Delete Task From Database
    """
    query = f"DELETE FROM tasks WHERE id = {task_id}"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
