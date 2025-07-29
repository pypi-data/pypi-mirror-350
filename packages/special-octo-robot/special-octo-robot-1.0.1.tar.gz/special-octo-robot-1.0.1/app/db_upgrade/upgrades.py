from app.application import list_tables
from app.database import delete_table
from app.database import initialize
from app.database import insert_into_table
from app.database import rename_table
from app.utility import convert_time_to_epoch


def upgrade_0_5_1(cur):

    for table in list_tables():
        temp_table = "temp_" + table
        initialize(temp_table)

        query = f"SELECT * FROM {table}"
        res = cur.execute(query).fetchall()

        for each in res:
            deadline = each[5]
            completed = each[8]
            parent_id = each[2]
            if deadline == "None":
                deadline = "0"
            else:
                deadline = str(convert_time_to_epoch(deadline))

            if completed == "None":
                completed = "0"
            else:
                completed = str(convert_time_to_epoch(completed))

            if parent_id == None:
                parent_id = "NULL"

            task = (
                str(each[0]),
                f"'{each[1]}'",
                str(parent_id),
                f"'{each[3]}'",
                f"'{each[4]}'",
                deadline,
                str(each[6]),
                f"'{each[7]}'",
                completed,
                str(each[9]),
            )
            columns = [
                "id",
                "title",
                "parent_id",
                "description",
                "status",
                "deadline",
                "priority",
                "label",
                "completed",
                "subtasks",
            ]
            insert_into_table(temp_table, columns, task)

        delete_table(table)
        rename_table(temp_table, table)


def upgrade_0_6_3(cur):
    """
    Upgrade the database to version 0.6.3
    """
    for table in list_tables():
        # Drop the existing trigger
        cur.execute(f"DROP TRIGGER IF EXISTS initialize_completed_column_{table};")

        # Add a new trigger to check the value of completed before updating it
        cur.execute(
            f"""
            CREATE TRIGGER initialize_completed_column_{table}
            AFTER INSERT ON {table}
            FOR EACH ROW
            BEGIN
                UPDATE {table} SET completed = NEW.deadline WHERE id = NEW.id AND NEW.completed == 0;
            END;
            """,
        )


def upgrade_1_0_0(cur):
    """
    Upgrade the database to version 1.0.0
    """
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            table_name VARCHAR NOT NULL,
            start_datetime INTEGER NOT NULL,
            end_datetime INTEGER NOT NULL
        )""",
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS session_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            application_name VARCHAR NOT NULL,
            duration INTEGER NOT NULL,
            FOREIGN KEY(session_id) REFERENCES sessions(session_id)
            ON DELETE CASCADE
        )""",
    )
    cur.execute(
        f"CREATE INDEX IF NOT EXISTS session_id_session on sessions(session_id);",
    )
    cur.execute(
        f"CREATE INDEX IF NOT EXISTS session_id_data on session_data(session_id);",
    )
    tables = list_tables()
    for table in tables:
        # Drop the existing trigger
        cur.execute(f"DROP INDEX IF EXISTS title_{table};")

        # Add a new trigger to check the value of completed before updating it
        cur.execute(
            f"""
            CREATE INDEX IF NOT EXISTS index_{table} ON {table}(id, title);
            """,
        )
