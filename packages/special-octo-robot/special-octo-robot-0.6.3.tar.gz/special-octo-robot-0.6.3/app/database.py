import sqlite3

from app.constants import db_path

# we should have separate functions to create triggers and indexes


def initialize(table_name: str) -> None:
    """
    Initialize the database with all the necessary tables.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        f"""CREATE TABLE {table_name}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL, parent_id INTEGER,
        description TEXT DEFAULT 'None',
        status VARCHAR DEFAULT 'Pending',
        deadline INTEGER DEFAULT 0,
        priority INTEGER DEFAULT 0,
        label VARCHAR DEFAULT 'None',
        completed INTEGER DEFAULT 0,
        subtasks INTEGER DEFAULT 0
        )""",
    )
    cur.execute(
        f"""
        CREATE TRIGGER initialize_completed_column_{table_name}
        AFTER INSERT ON {table_name}
        FOR EACH ROW
        BEGIN
            UPDATE {table_name} SET completed = NEW.deadline WHERE id = NEW.id AND NEW.completed == 0;
        END;
    """,
    )
    cur.execute(f"CREATE INDEX title_{table_name} on {table_name}(title);")
    conn.commit()


def list_tables() -> list:
    """
    List all the tables in the database.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.commit()
    return res


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
    conn.commit()
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


def delete_task(table: str, task_id: int) -> None:
    """
    Delete Task From Database
    """
    query = f"DELETE FROM {table} WHERE id = {task_id}"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()


def delete_table(table_name: str) -> None:
    """
    Delete Table From Database
    """
    query = f"DROP TABLE {table_name}; "
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    cur.execute(f"DROP INDEX IF EXISTS title_{table_name}")
    cur.execute(f"DROP TRIGGER IF EXISTS initialize_completed_column_{table_name};")
    conn.commit()


def rename_table(old_table_name: str, new_table_name: str) -> None:
    """
    Rename Table In Database
    """
    query = f"ALTER TABLE {old_table_name} RENAME TO {new_table_name}"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    try:
        cur.execute(
            f"ALTER INDEX title_{old_table_name} RENAME TO title_{new_table_name};",
        )
        cur.execute(
            f"ALTER TRIGGER initialize_completed_column_{old_table_name} RENAME TO initialize_completed_column_{new_table_name};",
        )
    except:
        # the code will reach here probably because of the index, so for now as a temp fix we will create the index instead of throwing an error.
        # will remove this in the later versions
        cur.execute(f"CREATE INDEX title_{new_table_name} on {new_table_name}(title);")
    conn.commit()
