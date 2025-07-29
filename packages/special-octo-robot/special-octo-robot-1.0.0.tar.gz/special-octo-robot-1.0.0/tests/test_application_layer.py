import os
import unittest
from app.constants import path, db_path
from app.utility import convert_time_to_epoch, get_relative_date_string
from app.database import add_session_data, initialize, insert_into_table, add_session
from app.application import list_tasks, add_tasks, search_task, get_subtasks, handle_delete, update_task, list_sessions, get_session_data
from datetime import datetime, timedelta

def create_db():
    os.makedirs(path, exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)
    initialize("tasks")

def fill_db():
    add_tasks(title = "Task 1", description="Description 1", priority=1)
    add_tasks(title = "Task 2", description="Description 2", priority=4, today=True)
    add_tasks(title = "Task 3", description="Description 3", priority=2, week=True)
    future_date = datetime.now() + timedelta(days=10)
    add_tasks(title = "Task 4", description="Description 4", priority=3, deadline=future_date.strftime("%Y-%m-%d"))
    add_tasks(title = "Task 5", description="Description 5", priority=5, completed=True)
    add_tasks(title = "Task 6", description="Description 6", inprogress=True)
    add_tasks(title = "Task 7", description="Description 7", pending=True)
    add_tasks(title = "Task 8", priority=3, deadline='2000-09-11')
    add_tasks(title='Child of task 1', parent={"id":1}, label='Label1')
    add_tasks(title='Child of child task 1', parent={"id": 9}, week=True)
    insert_into_table(table="tasks", columns=["title", "completed", "status"], values=["'Task 9'", str(convert_time_to_epoch("2024-08-25")), "'Completed'"])
    add_session(task_id=2,table_name="tasks", start_datetime=1724985000, end_datetime=1724985900)
    add_session(task_id=2,table_name="tasks", start_datetime=1724989000, end_datetime=1724990000)
    add_session(task_id=5, table_name="tasks", start_datetime=1725985000, end_datetime=1725985900)
    add_session(task_id=6, table_name="tasks", start_datetime=1726989000, end_datetime=1726990000)
    add_session_data(session_id=1, application_name="Pomodoro", duration=900)
    add_session_data(session_id=1, application_name="Pomodoro-2", duration=903)
    add_session_data(session_id=2, application_name="CODE", duration=50)
    add_session_data(session_id=2, application_name="WhatsAPP", duration=90)

class ListTasks(unittest.TestCase):
    def test_list_task_with_empty_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        # Test with no entries in table
        self.assertEqual(list_tasks(), [])

    def test_list_task_with_filled_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(list_tasks(), [
            {
                    "id": 6,
                    "title": "Task 6",
                    "parent_id": None,
                    "status": "In Progress",
                    "deadline": "None",
                    "priority": 0,
                    "label": "None",
                    "description": "Description 6",
                    "subtasks": 0,
                },
                {
                    "id": 1,
                    "title": "Task 1",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "None",
                    "priority": 1,
                    "label": "None",
                    "description": "Description 1",
                    "subtasks": 1,
                },
                {
                    "id": 7,
                    "title": "Task 7",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "None",
                    "priority": 0,
                    "label": "None",
                    "description": "Description 7",
                    "subtasks": 0,
                },
                {
                    "id": 8,
                    "title": "Task 8",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "11-09-2000",
                    "priority": 3,
                    "label": "None",
                    "description": "None",
                    "subtasks": 0,
                },
                {
                    "id": 2,
                    "title": "Task 2",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "31-08-2024",
                    "priority": 4,
                    "label": "None",
                    "description": "Description 2",
                    "subtasks": 0,
                },
                {
                    "id": 3,
                    "title": "Task 3",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "01-09-2024",
                    "priority": 2,
                    "label": "None",
                    "description": "Description 3",
                    "subtasks": 0,
                },
                {
                    "id": 4,
                    "title": "Task 4",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "10-09-2024",
                    "priority": 3,
                    "label": "None",
                    "description": "Description 4",
                    "subtasks": 0,
                },
            ]
        )

    def test_list_task_with_priority_and_today(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(list_tasks(priority=1, today=True), [])

    def test_list_task_with_priority(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(list_tasks(priority=1),[
                {
                    "id": 1,
                    "title": "Task 1",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "None",
                    "priority": 1,
                    "label": "None",
                    "description": "Description 1",
                    "subtasks": 1,
                }
            ])

    def test_list_task_with_today(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(list_tasks(today=True), [
                {
                    "id": 2,
                    "title": "Task 2",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "31-08-2024",
                    "priority": 4,
                    "label": "None",
                    "description": "Description 2",
                    "subtasks": 0,
                }
            ]
        )

    def test_list_task_with_week(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        self.maxDiff = None

        self.assertEqual(list_tasks(week=True, subtasks=True), [
                {
                    "id": 2,
                    "title": "Task 2",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "31-08-2024",
                    "priority": 4,
                    "label": "None",
                    "description": "Description 2",
                    "subtasks": 0,
                },
                {
                    "id": 3,
                    "title": "Task 3",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "01-09-2024",
                    "priority": 2,
                    "label": "None",
                    "description": "Description 3",
                    "subtasks": 0,
                },
                {
                    "id": 10,
                    "title": "Child of child task 1",
                    "parent_id": 9,
                    "status": "Pending",
                    "deadline": "01-09-2024",
                    "priority": 0,
                    "label": "None",
                    "description": "None",
                    "subtasks": 0,
                },
            ]
                         )

    def test_list_task_with_status(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        self.maxDiff = None

        self.assertEqual(list_tasks(inprogress=True, completed=True), [
            {
                "id": 6,
                "title": "Task 6",
                "parent_id": None,
                "status": "In Progress",
                "deadline": "None",
                "priority": 0,
                "label": "None",
                "description": "Description 6",
                "subtasks": 0,
            },
            {
                "id": 11,
                "title": "Task 9",
                "parent_id": None,
                "status": "Completed",
                "deadline": "None",
                "priority": 0,
                "label": "None",
                "description": "None",
                "subtasks": 0,
            },
            {
                "id": 5,
                "title": "Task 5",
                "parent_id": None,
                "status": "Completed",
                "deadline": "None",
                "priority": 5,
                "label": "None",
                "description": "Description 5",
                "subtasks": 0,
            },
            ]
        )

    def test_list_task_with_label(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(list_tasks(label='Label1', subtasks=True), [
                {
                    "id": 9,
                    "title": "Child of task 1",
                    "parent_id": 1,
                    "status": "Pending",
                    "deadline": "None",
                    "priority": 0,
                    "label": "Label1",
                    "description": "None",
                    "subtasks": 1,
                }
            ]
        )
    
    def test_list_task_with_relative_deadline(self) -> None:
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        
        self.assertEqual(list_tasks(date=get_relative_date_string(-6), completed=True), [
                 {
                "id": 11,
                "title": "Task 9",
                "parent_id": None,
                "status": "Completed",
                "deadline": "None",
                "priority": 0,
                "label": "None",
                "description": "None",
                "subtasks": 0,
            }
            ]
        )

class AddTasks(unittest.TestCase):
    def test_adding_task_with_single_quotes_in_description(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()

        self.assertEqual(add_tasks(title='Dummy Task', description="'Description'"), None)

    def test_adding_task_with_special_characters(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()

        self.assertEqual(add_tasks(title='Dummy Task', description="$ / \ "), None)

class SearchTask(unittest.TestCase):
    def test_search_task_with_empty_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()

        self.assertEqual(search_task(1, "tasks"), {})

    def test_search_task_with_filled_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(search_task(1, "tasks"), {
                "id": 1,
                "title": "Task 1",
                "description": "Description 1",
                "status": "Pending",
                "deadline": "None",
                "priority": 1,
                "label": "None",
                "completed": "None",
                "parent_id": None,
                "subtasks": 1,
            }
        )

    def test_search_task_with_invalid_id(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(search_task(100, "tasks"), {})

class GetSubtasks(unittest.TestCase):
    def test_get_subtasks_with_empty_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()

        self.assertEqual(get_subtasks(1, "tasks"), [])

    def test_get_subtasks_with_filled_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(
            get_subtasks(1, "tasks"),
            [
                {
                    'id': 9,
                    'title': 'Child of task 1',
                    'status': 'Pending',
                    'deadline': 'None',
                    'priority': 0,
                    'label': 'Label1',
                    'description': 'None',
                    'subtasks': 1,
                    'parent_id': 1
                }
            ]
        )

    def test_get_subtasks_with_invalid_id(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(get_subtasks(100, "tasks"), [])

class HandleDelete(unittest.TestCase):
    def test_with_filled_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        # test with valid id
        handle_delete({"id": 1, "parent_id": None}, "tasks")
        self.assertEqual(list_tasks(), [
              {
                "id": 6,
                "title": "Task 6",
                "parent_id": None,
                "status": "In Progress",
                "deadline": "None",
                "priority": 0,
                "label": "None",
                "description": "Description 6",
                "subtasks": 0,
            },
            {
                "id": 7,
                "title": "Task 7",
                "parent_id": None,
                "status": "Pending",
                "deadline": "None",
                "priority": 0,
                "label": "None",
                "description": "Description 7",
                "subtasks": 0,
            },
            {
                "id": 8,
                "title": "Task 8",
                "parent_id": None,
                "status": "Pending",
                "deadline": "11-09-2000",
                "priority": 3,
                "label": "None",
                "description": "None",
                "subtasks": 0,
            },
            {
                "id": 2,
                "title": "Task 2",
                "parent_id": None,
                "status": "Pending",
                "deadline": "31-08-2024",
                "priority": 4,
                "label": "None",
                "description": "Description 2",
                "subtasks": 0,
            },
            {
                "id": 3,
                "title": "Task 3",
                "parent_id": None,
                "status": "Pending",
                "deadline": "01-09-2024",
                "priority": 2,
                "label": "None",
                "description": "Description 3",
                "subtasks": 0,
            },
            {
                "id": 4,
                "title": "Task 4",
                "parent_id": None,
                "status": "Pending",
                "deadline": "10-09-2024",
                "priority": 3,
                "label": "None",
                "description": "Description 4",
                "subtasks": 0,
            },
        ])
        self.assertEqual(list_tasks(week=True, subtasks=True), [
            {
                "id": 2,
                "title": "Task 2",
                "parent_id": None,
                "status": "Pending",
                "deadline": "31-08-2024",
                "priority": 4,
                "label": "None",
                "description": "Description 2",
                "subtasks": 0,
            },
            {
                "id": 3,
                "title": "Task 3",
                "parent_id": None,
                "status": "Pending",
                "deadline": "01-09-2024",
                "priority": 2,
                "label": "None",
                "description": "Description 3",
                "subtasks": 0,
            },
        ])

    def test_subtask_deletion(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        # test with subtask id
        handle_delete({"id": 9, "parent_id": 1}, "tasks")
        self.assertEqual(search_task(1, "tasks"), {
                "id": 1,
                "title": "Task 1",
                "description": "Description 1",
                "status": "Pending",
                "deadline": "None",
                "priority": 1,
                "label": "None",
                "completed": "None",
                "parent_id": None,
                "subtasks": 0,
            })


class HandleModify(unittest.TestCase):
    def test_cascading_effect_with_filled_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        task = search_task(1, "tasks")
        task['status'] = 'Completed'
        update_task(task, "tasks")   # cascading update
        self.assertEqual(search_task(1, "tasks"), {'id': 1, 'title': 'Task 1', 'description': 'Description 1', 'status': 'Completed', 'deadline': 'None', 'priority': 1, 'label': 'None', 'completed': '31-08-2024', 'parent_id': None, 'subtasks': 1})
        self.assertEqual(get_subtasks(1, "tasks"), [{'id': 9, 'title': 'Child of task 1', 'status': 'Completed', 'deadline': 'None', 'priority': 0, 'label': 'Label1', 'description': 'None', 'subtasks': 1, 'parent_id': 1}])
        self.assertEqual(get_subtasks(9, "tasks"), [{'id': 10, 'title': 'Child of child task 1', 'status': 'Completed', 'deadline': '01-09-2024', 'priority': 0, 'label': 'None', 'description': 'None', 'subtasks': 0, 'parent_id': 9}])

class ListSessions(unittest.TestCase):
    def test_list_sessions_with_empty_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        # Test with no sessions in table
        self.assertEqual(list_sessions("tasks"), [])

    def test_list_sessions_with_filled_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        sessions = list_sessions("tasks")
        self.assertTrue(isinstance(sessions, list))
        expected_sessions = [
            {
            "session_id": 4,
            "task_name": "Task 6",
            "start_datetime": "12:40, 22/9/2024",
            "end_datetime": "12:56, 22/9/2024",
            "duration": "16 mins, 40 secs",
            },
            {
            "session_id": 3,
            "task_name": "Task 5",
            "start_datetime": "21:46, 10/9/2024",
            "end_datetime": "22:01, 10/9/2024",
            "duration": "15 mins",
            },
            {
            "session_id": 2,
            "task_name": "Task 2",
            "start_datetime": "09:06, 30/8/2024",
            "end_datetime": "09:23, 30/8/2024",
            "duration": "16 mins, 40 secs",
            },
            {
            "session_id": 1,
            "task_name": "Task 2",
            "start_datetime": "08:00, 30/8/2024",
            "end_datetime": "08:15, 30/8/2024",
            "duration": "15 mins",
            },
        ]
        # Only check the first 4 sessions for exact match (since fill_db inserts 4 sessions)
        for i, expected in enumerate(expected_sessions):
            for key in expected:
                self.assertEqual(sessions[i][key], expected[key])

    def test_list_sessions_with_task_id(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        # Task 2 has two sessions in fill_db
        sessions = list_sessions("tasks", task_id=2)
        self.assertTrue(isinstance(sessions, list))
        self.assertEqual(len(sessions), 2)
        for session in sessions:
            self.assertEqual(session["task_name"], "Task 2")

    def test_list_sessions_with_invalid_task_id(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        sessions = list_sessions("tasks", task_id=999)
        self.assertEqual(sessions, [])

class GetSessionData(unittest.TestCase):
    def test_get_session_data_with_valid_session_id(self):
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        create_db()
        fill_db()
        session_data = get_session_data(1)
        self.assertIsInstance(session_data, dict)
        self.assertIn("data", session_data)
        self.assertIsInstance(session_data["data"], list)
        expected = [
            {"application_name": "Pomodoro", "duration": "15 mins"},
            {"application_name": "Pomodoro-2", "duration": "15 mins, 3 secs"},
        ]
        self.assertEqual(session_data["data"], expected)

    def test_get_session_data_with_valid_session_id_2(self):
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        create_db()
        fill_db()
        session_data = get_session_data(2)
        self.assertIsInstance(session_data, dict)
        self.assertIn("data", session_data)
        self.assertIsInstance(session_data["data"], list)
        expected = [
            {"application_name": "CODE", "duration": "50 secs"},
            {"application_name": "WhatsAPP", "duration": "1 mins, 30 secs"},
        ]
        self.assertEqual(session_data["data"], expected)

    def test_get_session_data_with_invalid_session_id(self):
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        create_db()
        fill_db()
        session_data = get_session_data(9999)
        self.assertIsInstance(session_data, dict)
        self.assertEqual(session_data["data"], [])


if __name__ == '__main__':
    unittest.main()
